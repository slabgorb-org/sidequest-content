#!/usr/bin/env python3
"""Audit and (optionally) repair POI slug↔filename mismatches.

The runtime resolver (sidequest-server/sidequest/server/rest.py) builds POI
URLs as `assets/poi/<slug>.png`. When the rendered file on disk is named
differently — typically because the prose title was used to derive the
filename ("A Bridge over the Seine" → `a_bridge_over_the_seine.png`) while
the YAML slug normalized differently (`bridge_over_the_seine`) — the URL
404s in the lobby and reference pages.

This script:
  1. Walks every world under `genre_packs/*/worlds/*`
  2. Reads POI slugs from `history.yaml` (entries with `slug` + `visual_prompt`)
  3. Compares against `assets/poi/*.png` in that world
  4. For each missing-render slug, looks for a single unambiguous filename
     match using a normalized form (lowercase ASCII, strip diacritics,
     hyphen↔underscore, optional `the_`/`a_` prefix, optional `_the_` infix)
  5. With --apply, renames via plain `mv` (POI PNGs are gitignored per
     sidequest-content/CLAUDE.md — they live on R2; only the YAML spec is
     tracked)

Run from the sidequest-content repo root:
    python3 tools/audit_poi_slug_mismatches.py          # dry-run report
    python3 tools/audit_poi_slug_mismatches.py --apply  # actually rename

Cases the script will NOT auto-rename (reported for manual fix):
  - More than one candidate matches the slug under normalization
  - A rendered file matches no slug at all (orphan PNG)
  - The slug has zero filename matches (genuine missing render)

NOTE: This renames the local file only. After applying, re-run the R2
upload (`scripts/r2_sync_packs.py` from the orchestrator) and consider
deleting the old object name from R2 to avoid stale references.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml


def normalize(s: str) -> str:
    """Lowercase ASCII, strip diacritics, collapse hyphen/underscore, strip
    leading article ("the_"/"a_"), and remove the infix "_the_"."""
    # strip diacritics
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    # unify separators
    s = s.replace("-", "_")
    # strip leading article
    for prefix in ("the_", "a_"):
        if s.startswith(prefix):
            s = s[len(prefix) :]
            break
    # collapse "_the_" infix (handles "wazan_the_capital" ↔ "wazan_capital")
    s = s.replace("_the_", "_")
    return s


def collect_poi_slugs(world_dir: Path) -> dict[str, str]:
    """Return {slug: source_file} for every POI entry in this world's yamls.

    A POI entry is a dict with `slug` and a `visual_prompt` (the renderable
    contract). Plain `slug` fields elsewhere (e.g. region slugs) are skipped.
    """
    slugs: dict[str, str] = {}
    for yf in world_dir.glob("*.yaml"):
        try:
            data = yaml.safe_load(yf.read_text(encoding="utf-8"))
        except Exception:
            continue

        def walk(node) -> None:
            if isinstance(node, dict):
                if (
                    "slug" in node
                    and isinstance(node["slug"], str)
                    and "visual_prompt" in node
                ):
                    slugs.setdefault(node["slug"], yf.name)
                for v in node.values():
                    walk(v)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)
    return slugs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually rename files via `git mv` (default: dry-run report)",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("genre_packs"),
        help="Genre packs root (default: genre_packs)",
    )
    args = parser.parse_args()

    if not args.root.exists():
        print(f"error: {args.root} does not exist (run from repo root)", file=sys.stderr)
        return 2

    total_renamed = 0
    total_ambiguous = 0
    total_orphan = 0
    total_missing = 0

    for world_yaml in sorted(args.root.glob("*/worlds/*/world.yaml")):
        world_dir = world_yaml.parent
        pack = world_dir.parts[-3]
        world = world_dir.parts[-1]
        label = f"{pack}/{world}"

        poi_dir = world_dir / "assets" / "poi"
        if not poi_dir.exists():
            continue

        slugs = collect_poi_slugs(world_dir)
        files = list(poi_dir.glob("*.png"))
        file_by_stem = {f.stem: f for f in files}

        # build normalized index of available filenames
        norm_to_files: dict[str, list[Path]] = defaultdict(list)
        for f in files:
            norm_to_files[normalize(f.stem)].append(f)

        rendered_used: set[Path] = set()
        renames: list[tuple[Path, Path]] = []
        ambiguous: list[tuple[str, list[Path]]] = []
        missing: list[str] = []

        for slug in sorted(slugs):
            if slug in file_by_stem:
                rendered_used.add(file_by_stem[slug])
                continue
            candidates = norm_to_files.get(normalize(slug), [])
            # avoid claiming a file already targeted by another slug this run
            candidates = [c for c in candidates if c not in rendered_used]
            if len(candidates) == 1:
                src = candidates[0]
                dst = src.with_name(f"{slug}.png")
                renames.append((src, dst))
                rendered_used.add(src)
            elif len(candidates) > 1:
                ambiguous.append((slug, candidates))
            else:
                missing.append(slug)

        orphans = [f for f in files if f not in rendered_used]

        if not (renames or ambiguous or orphans or missing):
            continue

        print(f"\n=== {label} ===")
        for src, dst in renames:
            total_renamed += 1
            verb = "RENAME" if args.apply else "would-rename"
            print(f"  {verb}: {src.name}  →  {dst.name}")
            if args.apply:
                # POI PNGs are gitignored (live on R2 per
                # sidequest-content/CLAUDE.md), so plain mv — git mv would
                # error with "not under version control".
                try:
                    src.rename(dst)
                except OSError as exc:
                    print(f"    rename failed: {exc}", file=sys.stderr)
                    return 1
        for slug, cands in ambiguous:
            total_ambiguous += 1
            names = ", ".join(c.name for c in cands)
            print(f"  AMBIGUOUS: slug={slug}  candidates=[{names}]  — fix manually")
        for slug in missing:
            total_missing += 1
            print(f"  NO-RENDER: slug={slug}  — needs a POI render pass")
        for f in orphans:
            total_orphan += 1
            print(f"  ORPHAN-PNG: {f.name}  — no slug references it")

    print(
        f"\nSummary: renamed={total_renamed} "
        f"ambiguous={total_ambiguous} "
        f"missing-renders={total_missing} "
        f"orphan-pngs={total_orphan}"
        + ("" if args.apply else "  (dry-run; pass --apply to execute)")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

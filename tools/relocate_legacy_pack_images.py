#!/usr/bin/env python3
"""Relocate POIs and creatures from pack-level legacy `images/` to the
canonical `worlds/<world>/assets/` layout.

Historical context: `scripts/render_common.py` only bridges POIs (image_subdir
== "poi") to the world-tier layout; creatures and any older POI renders that
predated that bridge ended up at `genre_packs/<pack>/images/poi/*.png` or
`images/creatures/*.png`. The server's POI resolver only reads
`worlds/<world>/assets/poi/`, so these files are invisible to runtime even
though they exist on disk.

Portraits are intentionally NOT touched — `images/portraits/` is still where
the portrait renderer writes today and where the portrait_manifest loader
expects them.

This script:
  1. Walks every `<pack>/images/<kind>/*.png` (kind = poi or creatures)
     under --src-root.
  2. For each file, computes an ASCII-folded slug from the filename.
  3. Looks up which world in that pack owns a matching slug (collected from
     each world's *.yaml files: any dict with `slug` + `visual_prompt`).
  4. Copies the file to `--dst-root/genre_packs/<pack>/worlds/<world>/assets/
     <kind>/<slug>.png` (preserving timestamps).
  5. With --delete-source, removes the source after a successful copy.

Files with no matching slug, files matching multiple worlds, or files whose
destination already exists are reported and skipped — fix manually.

Defaults to dry-run. Pass --apply to actually copy.

Usage:
    # In-place oq-1 cleanup (POIs and creatures from oq-1's own images/)
    python3 tools/relocate_legacy_pack_images.py
    python3 tools/relocate_legacy_pack_images.py --apply --delete-source

    # Cross-clone import (oq-2 has assets oq-1 doesn't)
    python3 tools/relocate_legacy_pack_images.py \\
        --src-root /Users/slabgorb/Projects/oq-2/sidequest-content \\
        --dst-root /Users/slabgorb/Projects/oq-1/sidequest-content \\
        --apply

Per project rules, PNGs are NOT git-tracked — R2 is the source of truth.
After running this, re-run `scripts/r2_sync_packs.py` from the orchestrator.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

import yaml


def ascii_fold(s: str) -> str:
    folded = unicodedata.normalize("NFKD", s)
    stripped = "".join(c for c in folded if not unicodedata.combining(c))
    return stripped.encode("ascii", errors="ignore").decode("ascii")


def normalize_key(s: str) -> str:
    """Slug-comparable key: ASCII, lowercase, hyphen→underscore, strip
    leading `the_`/`a_`, strip `_the_` infix."""
    s = ascii_fold(s).lower().replace("-", "_")
    for prefix in ("the_", "a_"):
        if s.startswith(prefix):
            s = s[len(prefix) :]
            break
    return s.replace("_the_", "_")


def collect_world_slugs(world_dir: Path) -> set[str]:
    slugs: set[str] = set()

    def walk(node) -> None:
        if isinstance(node, dict):
            if (
                "slug" in node
                and isinstance(node["slug"], str)
                and "visual_prompt" in node
            ):
                slugs.add(node["slug"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    for yf in world_dir.glob("*.yaml"):
        try:
            walk(yaml.safe_load(yf.read_text(encoding="utf-8")))
        except Exception:
            continue
    return slugs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--src-root",
        type=Path,
        default=Path.cwd(),
        help="sidequest-content root to read pack-level images/ from "
        "(default: cwd)",
    )
    parser.add_argument(
        "--dst-root",
        type=Path,
        default=Path.cwd(),
        help="sidequest-content root to write worlds/<world>/assets/ into "
        "(default: cwd; same as --src-root for in-place moves)",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually copy (default: dry-run report)",
    )
    parser.add_argument(
        "--delete-source",
        action="store_true",
        help="After a successful copy, delete the source file (turns copy "
        "into move). Cross-clone runs typically leave this off.",
    )
    parser.add_argument(
        "--kind",
        choices=("poi", "creatures", "both"),
        default="both",
        help="Which legacy subdir to migrate (default: both)",
    )
    args = parser.parse_args()

    src_root = args.src_root.resolve()
    dst_root = args.dst_root.resolve()

    if not (src_root / "genre_packs").is_dir():
        print(
            f"error: {src_root}/genre_packs does not exist", file=sys.stderr
        )
        return 2

    kinds = ("poi", "creatures") if args.kind == "both" else (args.kind,)

    moved = collided = ambiguous = orphan = 0

    for pack_dir in sorted((src_root / "genre_packs").iterdir()):
        if not pack_dir.is_dir():
            continue
        pack = pack_dir.name

        # build slug→world index for this pack
        dst_pack = dst_root / "genre_packs" / pack
        dst_worlds_root = dst_pack / "worlds"
        if not dst_worlds_root.is_dir():
            continue
        slug_to_worlds: dict[str, list[str]] = defaultdict(list)
        for wd in sorted(dst_worlds_root.iterdir()):
            if not wd.is_dir():
                continue
            for slug in collect_world_slugs(wd):
                slug_to_worlds[normalize_key(slug)].append(wd.name)

        header_printed = False
        for kind in kinds:
            src_dir = pack_dir / "images" / kind
            if not src_dir.is_dir():
                continue
            for src_file in sorted(src_dir.glob("*.png")):
                key = normalize_key(src_file.stem)
                candidate_worlds = slug_to_worlds.get(key, [])

                if not header_printed:
                    print(f"\n=== {pack} ===")
                    header_printed = True

                if not candidate_worlds:
                    print(f"  ORPHAN: images/{kind}/{src_file.name}  "
                          f"(no matching slug in any world)")
                    orphan += 1
                    continue
                if len(set(candidate_worlds)) > 1:
                    print(
                        f"  AMBIGUOUS: images/{kind}/{src_file.name}  "
                        f"(matches: {', '.join(sorted(set(candidate_worlds)))})"
                    )
                    ambiguous += 1
                    continue

                world = candidate_worlds[0]
                # the canonical slug is the un-normalized form — re-derive
                # by reading the world's slugs and picking the one whose
                # normalize_key matches
                world_dir = dst_worlds_root / world
                canonical_slug = next(
                    (s for s in collect_world_slugs(world_dir) if normalize_key(s) == key),
                    src_file.stem,
                )
                dst_dir = world_dir / "assets" / kind
                dst_file = dst_dir / f"{canonical_slug}.png"

                if dst_file.exists():
                    print(
                        f"  COLLISION: images/{kind}/{src_file.name}  "
                        f"→ {dst_file.relative_to(dst_root)}  (dest exists)"
                    )
                    collided += 1
                    continue

                verb = "COPY" if args.apply else "would-copy"
                rename_note = ""
                if canonical_slug != src_file.stem:
                    rename_note = f"  [slug-normalized: {canonical_slug}]"
                print(
                    f"  {verb}: images/{kind}/{src_file.name}  "
                    f"→ worlds/{world}/assets/{kind}/{canonical_slug}.png"
                    f"{rename_note}"
                )
                if args.apply:
                    dst_dir.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    if args.delete_source:
                        src_file.unlink()
                moved += 1

    print(
        f"\nSummary: {'moved' if args.apply else 'would-move'}={moved}  "
        f"collisions={collided}  ambiguous={ambiguous}  orphans={orphan}"
        + ("" if args.apply else "  (dry-run; pass --apply)")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

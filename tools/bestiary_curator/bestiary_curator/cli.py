"""``bestiary_curator`` CLI — curate one world's SRD corpus into a WWN bestiary.

Usage (from the sidequest-content repo root):

    python -m bestiary_curator genre_packs/<genre>/worlds/<world>
    python -m bestiary_curator genre_packs/<genre>/worlds/<world> --out curated.yaml

Writes the curated ``entries:`` document to stdout (or --out) and the GATE 1
drop audit to stderr. The output is the MECHANICAL skeleton; GATE 2 tone
curation and prose are the author's pass (see docs/bestiary-curation-recipe.md).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from .curate import curate_world


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bestiary_curator",
        description="Curate an SRD monster corpus into a per-world WWN bestiary "
        "via the world_register genre-truth gate.",
    )
    parser.add_argument(
        "world_dir",
        help="world directory holding corpus/monsters.yaml + world_register.yaml",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="write curated entries to this YAML file (default: stdout)",
    )
    args = parser.parse_args(argv)

    result = curate_world(args.world_dir)
    document = yaml.safe_dump({"entries": result.kept}, sort_keys=False, allow_unicode=True)

    if args.out is not None:
        args.out.write_text(document)
        print(f"wrote {len(result.kept)} curated entries -> {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(document)

    print(
        f"# GATE 1: kept {len(result.kept)}, dropped {len(result.dropped)}",
        file=sys.stderr,
    )
    for decision in result.dropped:
        print(f"#   DROP {decision.name}: {decision.reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

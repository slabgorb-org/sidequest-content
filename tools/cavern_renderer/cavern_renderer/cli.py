"""CLI: read room.yaml, generate sidecars, write derived block."""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

import yaml

from cavern_renderer import __version__
from cavern_renderer.cellular import FLOOR, gen_cave
from cavern_renderer.derive import find_exits, find_pois, floor_count
from cavern_renderer.render import render_grid_to_png


def process_room(room_yaml_path: Path) -> None:
    """Process one room. Idempotent: same input → byte-identical sidecars."""
    data = yaml.safe_load(room_yaml_path.read_text())
    room_type = data.get("room_type")
    if room_type == "settlement":
        return  # settlements have no PNG/mask
    if room_type != "cavern":
        raise ValueError(
            f"{room_yaml_path}: unknown room_type {room_type!r} "
            f"(expected 'cavern' or 'settlement')"
        )

    cellular = data["cellular"]
    width, height = cellular["size"]
    grid = gen_cave(
        width=width,
        height=height,
        seed=cellular["seed"],
        density=cellular.get("density", 0.55),
        cutoff=cellular.get("cutoff", 5),
        passes=cellular.get("passes", 4),
    )

    cell_size = cellular.get("cell_size", 28)
    stem = room_yaml_path.stem
    png_path = room_yaml_path.parent / f"{stem}.cavern.png"
    mask_path = room_yaml_path.parent / f"{stem}.mask.txt"

    render_grid_to_png(grid, png_path, cell_size=cell_size)
    mask_path.write_text(_grid_to_mask(grid))

    overrides = data.get("overrides") or {}
    derived_exits = overrides.get("exits") or _exits_to_yaml(find_exits(grid))
    derived_pois = overrides.get("pois") or [list(p) for p in find_pois(grid)]

    data["derived"] = {
        "floor_count": floor_count(grid),
        "exits": derived_exits,
        "pois": derived_pois,
        "generated_at": dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator_version": __version__,
    }
    room_yaml_path.write_text(yaml.safe_dump(data, sort_keys=False))


def _grid_to_mask(grid: list[list[int]]) -> str:
    return "\n".join(
        "".join("." if cell == FLOOR else "#" for cell in row) for row in grid
    ) + "\n"


def _exits_to_yaml(
    exits: dict[str, tuple[int, int] | None],
) -> dict[str, list[int] | None]:
    return {k: (list(v) if v else None) for k, v in exits.items()}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cavern renderer CLI")
    parser.add_argument("path", type=Path, help="room.yaml file or world directory")
    parser.add_argument(
        "--world",
        action="store_true",
        help="Treat path as a world dir; process every rooms/<id>.yaml within.",
    )
    args = parser.parse_args(argv)

    if args.world:
        rooms_dir = args.path / "rooms"
        if not rooms_dir.is_dir():
            print(f"error: {rooms_dir} does not exist", file=sys.stderr)
            return 2
        rooms = sorted(rooms_dir.glob("*.yaml"))
        for room in rooms:
            print(f"  processing {room.name}", file=sys.stderr)
            process_room(room)
        print(f"done: {len(rooms)} rooms", file=sys.stderr)
    else:
        process_room(args.path)
        print(f"done: {args.path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

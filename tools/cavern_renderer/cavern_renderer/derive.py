"""Derived data from cellular caverns: exits, POIs, floor count.

Ports the helpers in cave-gen.js: findExits, findPOIs, floorCount.
"""

from __future__ import annotations

import math

from cavern_renderer.cellular import FLOOR, WALL


def floor_count(grid: list[list[int]]) -> int:
    """Number of FLOOR cells in the grid."""
    return sum(1 for row in grid for cell in row if cell == FLOOR)


def find_exits(grid: list[list[int]]) -> dict[str, tuple[int, int] | None]:
    """First floor cell adjacent to each side of the bounding box.

    Returns the **border** cell (e.g. y=0 for north), not the interior
    floor cell. The border is always WALL after gen_cave; the exit
    coordinate is the wall position you'd carve through to reach the
    interior floor at (x, 1).
    """
    h = len(grid)
    w = len(grid[0]) if h else 0
    sides: dict[str, tuple[int, int] | None] = {
        "north": None,
        "south": None,
        "east": None,
        "west": None,
    }
    for x in range(1, w - 1):
        if sides["north"] is None and grid[1][x] == FLOOR:
            sides["north"] = (x, 0)
        if sides["south"] is None and grid[h - 2][x] == FLOOR:
            sides["south"] = (x, h - 1)
    for y in range(1, h - 1):
        if sides["west"] is None and grid[y][1] == FLOOR:
            sides["west"] = (0, y)
        if sides["east"] is None and grid[y][w - 2] == FLOOR:
            sides["east"] = (w - 1, y)
    return sides


def find_pois(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Chamber centers: floor cells with low local wall density.

    Mirrors cave-gen.js findPOIs: 5x5 neighborhood, fewer than 4 walls,
    and at least 3.5 cells apart from previously-found POIs.
    """
    h = len(grid)
    w = len(grid[0]) if h else 0
    out: list[tuple[int, int]] = []
    for y in range(2, h - 2):
        for x in range(2, w - 2):
            if grid[y][x] != FLOOR:
                continue
            walls = 0
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    if dx == 0 and dy == 0:
                        continue
                    if grid[y + dy][x + dx] == WALL:
                        walls += 1
            if walls < 4:
                if all(math.hypot(px - x, py - y) > 3.5 for px, py in out):
                    out.append((x, y))
    return out

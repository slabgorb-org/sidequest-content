"""Cellular automata cavern generator.

Port of maze-maker's Cellular class:
~/Projects/maze-maker/lib/maze_maker/cellular.rb

JS reference: cave-gen.js (function genCave) from the Claude Design hi-fi
handoff bundle.

Convention: 0 = floor, 1 = wall (matches maze_maker).
"""

from __future__ import annotations

import random

FLOOR = 0
WALL = 1


def gen_cave(
    width: int,
    height: int,
    seed: int,
    *,
    density: float = 0.55,
    cutoff: int = 5,
    passes: int = 4,
) -> list[list[int]]:
    """Generate a cellular-automaton cavern.

    Returns a (height x width) grid of FLOOR (0) or WALL (1).

    Determinism: same (width, height, seed, density, cutoff, passes) →
    identical output.

    Algorithm:
    1. Seed each interior cell as FLOOR with `density` probability.
    2. Force border cells to WALL.
    3. Run `passes` iterations of the standard CA rule:
       - cell becomes WALL if ≥ cutoff of 8 neighbors are walls
       - cell becomes FLOOR if < 4 of 8 neighbors are walls
    4. Flood-fill: keep largest connected FLOOR region; fill the rest.
    """
    rng = random.Random(seed)
    grid = [
        [FLOOR if rng.random() < density else WALL for _ in range(width)]
        for _ in range(height)
    ]
    # Borders forced to wall
    for x in range(width):
        grid[0][x] = WALL
        grid[height - 1][x] = WALL
    for y in range(height):
        grid[y][0] = WALL
        grid[y][width - 1] = WALL

    for _ in range(passes):
        grid = _ca_pass(grid, width, height, cutoff)

    grid = _keep_largest_floor_region(grid, width, height)
    return grid


def _ca_pass(grid: list[list[int]], width: int, height: int, cutoff: int) -> list[list[int]]:
    new = [row[:] for row in grid]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            walls = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    if grid[y + dy][x + dx] == WALL:
                        walls += 1
            if walls >= cutoff:
                new[y][x] = WALL
            elif walls < 4:
                new[y][x] = FLOOR
    return new


def _keep_largest_floor_region(
    grid: list[list[int]], width: int, height: int
) -> list[list[int]]:
    seen = [[False] * width for _ in range(height)]
    best: list[tuple[int, int]] = []
    for y in range(height):
        for x in range(width):
            if grid[y][x] != FLOOR or seen[y][x]:
                continue
            region = _flood(grid, seen, x, y, width, height)
            if len(region) > len(best):
                best = region
    keep = {(x, y) for x, y in best}
    out = [row[:] for row in grid]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == FLOOR and (x, y) not in keep:
                out[y][x] = WALL
    return out


def _flood(
    grid: list[list[int]],
    seen: list[list[bool]],
    sx: int,
    sy: int,
    width: int,
    height: int,
) -> list[tuple[int, int]]:
    stack = [(sx, sy)]
    region: list[tuple[int, int]] = []
    while stack:
        x, y = stack.pop()
        if x < 0 or y < 0 or x >= width or y >= height:
            continue
        if seen[y][x] or grid[y][x] != FLOOR:
            continue
        seen[y][x] = True
        region.append((x, y))
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return region

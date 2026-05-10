"""Tests for cellular CA cavern generator."""

from cavern_renderer.cellular import gen_cave, FLOOR, WALL


def test_gen_cave_returns_grid_of_correct_shape():
    grid = gen_cave(width=18, height=18, seed=1042)
    assert len(grid) == 18
    assert all(len(row) == 18 for row in grid)


def test_gen_cave_borders_are_walls():
    grid = gen_cave(width=18, height=18, seed=1042)
    for x in range(18):
        assert grid[0][x] == WALL
        assert grid[17][x] == WALL
    for y in range(18):
        assert grid[y][0] == WALL
        assert grid[y][17] == WALL


def test_gen_cave_is_deterministic_for_same_seed():
    g1 = gen_cave(width=18, height=18, seed=1042)
    g2 = gen_cave(width=18, height=18, seed=1042)
    assert g1 == g2


def test_gen_cave_differs_for_different_seed():
    g1 = gen_cave(width=18, height=18, seed=1042)
    g2 = gen_cave(width=18, height=18, seed=2099)
    assert g1 != g2


def test_gen_cave_only_floor_or_wall_values():
    grid = gen_cave(width=18, height=18, seed=1042)
    for row in grid:
        for cell in row:
            assert cell in (FLOOR, WALL)


def test_gen_cave_has_floor_cells():
    grid = gen_cave(width=18, height=18, seed=1042)
    floor_count = sum(1 for row in grid for cell in row if cell == FLOOR)
    assert floor_count > 50  # 18x18 with default density 0.55 → ≥50 floor cells


def test_gen_cave_floor_is_single_connected_component():
    """After flood-fill, all FLOOR cells should be reachable from any other."""
    grid = gen_cave(width=18, height=18, seed=1042)
    h, w = len(grid), len(grid[0])
    # find first floor
    start = None
    for y in range(h):
        for x in range(w):
            if grid[y][x] == FLOOR:
                start = (x, y)
                break
        if start:
            break
    assert start is not None
    # BFS from start, count reachable floors
    seen = {start}
    stack = [start]
    while stack:
        x, y = stack.pop()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and grid[ny][nx] == FLOOR and (nx, ny) not in seen:
                seen.add((nx, ny))
                stack.append((nx, ny))
    total_floor = sum(1 for row in grid for c in row if c == FLOOR)
    assert len(seen) == total_floor, "found isolated floor pocket"

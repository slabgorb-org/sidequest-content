"""Tests for derived data — exits, POIs."""

from cavern_renderer.cellular import gen_cave
from cavern_renderer.derive import find_exits, find_pois, floor_count


def test_find_exits_returns_dict_with_four_directions():
    grid = gen_cave(width=18, height=18, seed=1042)
    exits = find_exits(grid)
    assert set(exits.keys()) == {"north", "south", "east", "west"}


def test_find_exits_north_is_first_floor_adjacent_to_top_border():
    grid = [
        [1, 1, 1, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    exits = find_exits(grid)
    assert exits["north"] == (2, 0)


def test_find_exits_returns_none_for_blocked_side():
    grid = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1],
    ]
    exits = find_exits(grid)
    assert exits["north"] is None


def test_find_pois_returns_low_density_chamber_centers():
    grid = gen_cave(width=18, height=18, seed=1042)
    pois = find_pois(grid)
    assert len(pois) >= 1
    assert all(isinstance(p, tuple) and len(p) == 2 for p in pois)


def test_find_pois_are_spaced_apart():
    grid = gen_cave(width=18, height=18, seed=1042)
    pois = find_pois(grid)
    for i, (x1, y1) in enumerate(pois):
        for x2, y2 in pois[i + 1 :]:
            dist = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            assert dist > 3.5


def test_floor_count_matches_zero_cells():
    grid = [[0, 1], [1, 0]]
    assert floor_count(grid) == 2

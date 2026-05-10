"""Tests for Pillow PNG renderer."""

from pathlib import Path


from cavern_renderer.cellular import gen_cave
from cavern_renderer.render import render_grid_to_png


def test_render_dimensions_match_grid_times_cell_size(tmp_path):
    grid = gen_cave(width=18, height=18, seed=1042)
    out = tmp_path / "test.png"
    render_grid_to_png(grid, out, cell_size=28)

    from PIL import Image

    with Image.open(out) as img:
        assert img.size == (18 * 28, 18 * 28)
        assert img.mode == "RGB"


def test_render_is_byte_deterministic_for_same_input(tmp_path):
    grid = gen_cave(width=18, height=18, seed=1042)
    out1 = tmp_path / "a.png"
    out2 = tmp_path / "b.png"
    render_grid_to_png(grid, out1, cell_size=28)
    render_grid_to_png(grid, out2, cell_size=28)
    assert out1.read_bytes() == out2.read_bytes()


def test_render_handles_smaller_cell_size(tmp_path):
    grid = gen_cave(width=12, height=12, seed=99)
    out = tmp_path / "small.png"
    render_grid_to_png(grid, out, cell_size=16)

    from PIL import Image

    with Image.open(out) as img:
        assert img.size == (12 * 16, 12 * 16)


def test_render_creates_parent_dir_if_needed(tmp_path):
    grid = gen_cave(width=8, height=8, seed=1)
    out = tmp_path / "nested" / "dir" / "x.png"
    render_grid_to_png(grid, out, cell_size=20)
    assert out.exists()


def test_render_byte_matches_golden(tmp_path):
    """Pin output bytes for a known seed/dimensions/cell-size combo.

    If this fails after a render.py edit, decide: visual change intentional?
    Update the golden. Visual change accidental? Fix the regression.
    """
    grid = gen_cave(width=18, height=18, seed=1042)
    out = tmp_path / "test.png"
    render_grid_to_png(grid, out, cell_size=28)

    golden_path = Path(__file__).parent / "fixtures" / "golden_seed1042_18x18_28px.png"
    assert out.read_bytes() == golden_path.read_bytes()

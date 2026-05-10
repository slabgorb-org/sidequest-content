"""Pillow PNG renderer for cellular cavern grids.

Visual target: cavern stone in the dark sidequest-ui theme.
- floor cells: stone-gradient #3a3a4a base + deterministic per-cell grain
- walls:       inked #0e0e18 with stipple
- edges:       dark inked line at floor↔wall boundary
- vignette:    soft radial darkening at edges

The exact visual is allowed to drift from the JS reference; the contract
is reproducibility (same input → byte-identical PNG) and looking like
cavern stone in the SideQuest theme.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from cavern_renderer.cellular import FLOOR, WALL

_FLOOR_BASE = (58, 58, 74)  # #3a3a4a
_WALL_BASE = (14, 14, 24)  # #0e0e18
_GRAIN = (80, 80, 96)  # subtle dot
_INK = (0, 0, 0)
_GRID_LINE = (255, 255, 255)


def render_grid_to_png(
    grid: list[list[int]],
    output_path: Path,
    *,
    cell_size: int = 28,
    show_grid: bool = True,
) -> None:
    """Render a cellular cavern grid to a PNG file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    h = len(grid)
    w = len(grid[0]) if h else 0
    img = Image.new("RGB", (w * cell_size, h * cell_size), _WALL_BASE)
    draw = ImageDraw.Draw(img)

    # Floor cells with grain
    for y in range(h):
        for x in range(w):
            if grid[y][x] != FLOOR:
                continue
            px, py = x * cell_size, y * cell_size
            draw.rectangle(
                (px, py, px + cell_size - 1, py + cell_size - 1),
                fill=_FLOOR_BASE,
            )
            for i in range(6):
                hx = (x * 928371 + y * 7177 + i * 1733) % cell_size
                hy = (x * 31193 + y * 9241 + i * 4441) % cell_size
                v = (x * 19 + y * 7 + i * 11) % 5
                alpha_band = 0.06 + v * 0.04
                tint = _blend(_FLOOR_BASE, _GRAIN, alpha_band)
                draw.rectangle(
                    (px + hx, py + hy, px + hx + 1, py + hy + 1),
                    fill=tint,
                )

    # Inked edges around floor cells where they meet walls
    for y in range(h):
        for x in range(w):
            if grid[y][x] != FLOOR:
                continue
            px, py = x * cell_size, y * cell_size
            if y > 0 and grid[y - 1][x] == WALL:
                draw.line((px, py, px + cell_size - 1, py), fill=_INK)
            if y < h - 1 and grid[y + 1][x] == WALL:
                draw.line(
                    (px, py + cell_size - 1, px + cell_size - 1, py + cell_size - 1), fill=_INK
                )
            if x > 0 and grid[y][x - 1] == WALL:
                draw.line((px, py, px, py + cell_size - 1), fill=_INK)
            if x < w - 1 and grid[y][x + 1] == WALL:
                draw.line(
                    (px + cell_size - 1, py, px + cell_size - 1, py + cell_size - 1), fill=_INK
                )

    # Wall stipple
    for y in range(h):
        for x in range(w):
            if grid[y][x] != WALL:
                continue
            px, py = x * cell_size, y * cell_size
            for i in range(3):
                hx = (x * 1117 + y * 313 + i * 97) % cell_size
                hy = (x * 503 + y * 911 + i * 251) % cell_size
                draw.rectangle(
                    (px + hx, py + hy, px + hx + 1, py + hy + 1),
                    fill=(40, 40, 56),
                )

    # Optional grid overlay
    if show_grid:
        for x in range(w + 1):
            draw.line(
                ((x * cell_size, 0), (x * cell_size, h * cell_size)),
                fill=_blend((0, 0, 0), _GRID_LINE, 0.04),
            )
        for y in range(h + 1):
            draw.line(
                ((0, y * cell_size), (w * cell_size, y * cell_size)),
                fill=_blend((0, 0, 0), _GRID_LINE, 0.04),
            )

    img.save(output_path, "PNG", optimize=True)


def _blend(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return (
        int(a[0] * (1 - t) + b[0] * t),
        int(a[1] * (1 - t) + b[1] * t),
        int(a[2] * (1 - t) + b[2] * t),
    )

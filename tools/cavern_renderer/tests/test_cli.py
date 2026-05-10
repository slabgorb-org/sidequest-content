"""Tests for the CLI entrypoint."""

import shutil
from pathlib import Path

import pytest
import yaml

from cavern_renderer.cli import process_room

FIXTURE = Path(__file__).parent / "fixtures" / "sample_room.yaml"


@pytest.fixture
def room_in_tmp(tmp_path: Path) -> Path:
    dst = tmp_path / "sample_mouth.yaml"
    shutil.copy(FIXTURE, dst)
    return dst


def test_process_room_writes_png_and_mask_sidecars(room_in_tmp):
    process_room(room_in_tmp)
    assert (room_in_tmp.parent / "sample_mouth.cavern.png").exists()
    assert (room_in_tmp.parent / "sample_mouth.mask.txt").exists()


def test_process_room_writes_derived_block(room_in_tmp):
    process_room(room_in_tmp)
    data = yaml.safe_load(room_in_tmp.read_text())
    derived = data.get("derived")
    assert derived is not None
    assert "floor_count" in derived
    assert "exits" in derived
    assert "pois" in derived
    assert "generated_at" in derived
    assert "generator_version" in derived


def test_process_room_is_idempotent(room_in_tmp):
    process_room(room_in_tmp)
    png1 = (room_in_tmp.parent / "sample_mouth.cavern.png").read_bytes()
    mask1 = (room_in_tmp.parent / "sample_mouth.mask.txt").read_text()
    process_room(room_in_tmp)
    png2 = (room_in_tmp.parent / "sample_mouth.cavern.png").read_bytes()
    mask2 = (room_in_tmp.parent / "sample_mouth.mask.txt").read_text()
    assert png1 == png2
    assert mask1 == mask2


def test_process_room_skips_settlement_rooms(tmp_path):
    settlement = tmp_path / "confessional.yaml"
    settlement.write_text(
        yaml.safe_dump(
            {
                "id": "confessional",
                "name": "The Confessional",
                "room_type": "settlement",
                "description": "A small house keyed to humility.",
                "exits": [{"to": "sunden_square", "label": "out to the square"}],
            }
        )
    )
    process_room(settlement)  # should not raise
    assert not (tmp_path / "confessional.cavern.png").exists()
    assert not (tmp_path / "confessional.mask.txt").exists()


def test_mask_format_has_one_char_per_cell(room_in_tmp):
    process_room(room_in_tmp)
    mask_lines = (room_in_tmp.parent / "sample_mouth.mask.txt").read_text().splitlines()
    assert len(mask_lines) == 18
    assert all(len(line) == 18 for line in mask_lines)
    assert all(c in ".#" for line in mask_lines for c in line)

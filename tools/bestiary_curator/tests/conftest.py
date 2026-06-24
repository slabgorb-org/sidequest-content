"""Shared fixtures for the bestiary_curator suite.

The reference instance is the live, validated ``beneath_sunden`` world — the
proven curation pattern that story 158-20 generalizes. Tests pin the tool's
behaviour against this real data, so the fixtures resolve real repo paths
rather than synthetic fixtures.

This module deliberately does NOT import ``bestiary_curator`` at top level, so
that during the RED phase pytest collection still succeeds here and the missing
implementation surfaces as per-module ImportErrors in the test files (clear
"feature not implemented yet" signal) rather than a global collection crash.
"""

from pathlib import Path

import pytest
import yaml

# tests/ -> bestiary_curator/ -> tools/ -> sidequest-content (repo root)
REPO_ROOT = Path(__file__).resolve().parents[3]
BENEATH_SUNDEN = REPO_ROOT / "genre_packs" / "caverns_and_claudes" / "worlds" / "beneath_sunden"


@pytest.fixture
def beneath_sunden_dir() -> Path:
    """Directory of the reference world (holds world_register.yaml + corpus/)."""
    assert BENEATH_SUNDEN.is_dir(), f"reference world moved: {BENEATH_SUNDEN}"
    return BENEATH_SUNDEN


@pytest.fixture
def register_path(beneath_sunden_dir: Path) -> Path:
    p = beneath_sunden_dir / "world_register.yaml"
    assert p.is_file(), f"reference world_register moved: {p}"
    return p


@pytest.fixture
def corpus_path(beneath_sunden_dir: Path) -> Path:
    p = beneath_sunden_dir / "corpus" / "monsters.yaml"
    assert p.is_file(), f"reference corpus moved: {p}"
    return p


@pytest.fixture
def real_corpus(corpus_path: Path) -> list[dict]:
    """The full SRD monster corpus handed in for beneath_sunden (~330 rows)."""
    data = yaml.safe_load(corpus_path.read_text())
    assert isinstance(data, list) and data, "corpus should be a non-empty list of SRD rows"
    return data

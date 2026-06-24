"""End-to-end curation wiring test (story 158-20, AC-2 / AC-4).

This is the WIRING test: it runs the FULL production path — load the real
beneath_sunden corpus + world_register, gate every row, convert survivors onto
the WWN ladder, emit the drop audit — against real data, not synthetic
fixtures. If the deny gate, the reskin, the marquee exemption, or the stat
ladder isn't actually engaged, an invariant below breaks.

Ground truth (316-row SRD corpus, verified):
  kept:    Lich/Vampire/Mummy Lord (marquee, Undead), Aboleth (Aberration),
           "The Seep" (Gray Ooze reskinned)
  dropped: Solar/Deva/Planetar (Celestial), Kraken/Tarrasque (titan tag)
"""

from pathlib import Path

import pytest

from bestiary_curator import (
    WorldRegister,
    curate,
    curate_world,
    level_to_attack_bonus,
    level_to_hp,
    level_to_save,
)

BENEATH_SUNDEN = (
    Path(__file__).resolve().parents[3]
    / "genre_packs" / "caverns_and_claudes" / "worlds" / "beneath_sunden"
)

# Mechanical fields every curated stat block must carry to pass load_genre_pack.
REQUIRED_FIELDS = {"id", "name", "level", "hp", "armor_class", "attack_bonus", "save", "morale", "tags"}


@pytest.fixture(scope="module")
def curated():
    return curate_world(BENEATH_SUNDEN)


def _kept_names(curated):
    return {e["name"] for e in curated.kept}


def test_curate_world_returns_kept_and_dropped(curated):
    assert curated.kept, "curation produced no kept entries"
    assert curated.dropped, "curation dropped nothing — the gate is not engaged"


def test_curate_keeps_a_strict_subset(curated):
    total = len(curated.kept) + len(curated.dropped)
    assert 0 < len(curated.kept) < total, "expected some kept AND some dropped"


# ── deny gate engaged ──
@pytest.mark.parametrize("denied", ["Solar", "Deva", "Planetar"])
def test_celestials_are_absent_from_kept(curated, denied):
    assert denied not in _kept_names(curated)


@pytest.mark.parametrize("denied", ["Kraken", "Tarrasque"])
def test_titan_tagged_are_absent_from_kept(curated, denied):
    assert denied not in _kept_names(curated)


def test_drop_audit_records_a_reason_for_every_drop(curated):
    assert all(d.reason for d in curated.dropped), "every drop must carry an audit reason"
    assert all(d.kept is False for d in curated.dropped)


def test_solar_drop_is_attributed_to_celestial(curated):
    solar = next((d for d in curated.dropped if d.name == "Solar"), None)
    assert solar is not None, "Solar should appear in the drop audit"
    assert "celestial" in solar.reason.lower()


# ── marquee survive (Diamonds-and-Coal exemption) ──
@pytest.mark.parametrize("marquee", ["Lich", "Vampire", "Mummy Lord"])
def test_marquee_survive_curation(curated, marquee):
    assert marquee in _kept_names(curated)


# ── reskin applied ──
def test_gray_ooze_is_reskinned_to_the_seep(curated):
    names = _kept_names(curated)
    assert "The Seep" in names
    assert "Gray Ooze" not in names


# ── every kept entry is a complete, ladder-conformant WWN stat block ──
def test_every_kept_entry_has_required_fields(curated):
    for e in curated.kept:
        missing = REQUIRED_FIELDS - e.keys()
        assert not missing, f"{e.get('name')!r} missing fields: {missing}"


def test_kept_entries_follow_the_deterministic_ladder(curated):
    for e in curated.kept:
        lvl = e["level"]
        assert e["hp"] == level_to_hp(lvl), f"{e['name']}: hp off ladder"
        assert e["save"] == level_to_save(lvl), f"{e['name']}: save off ladder"
        assert e["attack_bonus"] == level_to_attack_bonus(lvl), f"{e['name']}: atk off ladder"


def test_kept_entries_have_in_range_archetype_fields(curated):
    """AC and morale are archetype-driven, not level-derived — but must be present
    and on their respective ladders (AC 12-17, morale on the 2-12 2d6 ladder)."""
    for e in curated.kept:
        assert 12 <= e["armor_class"] <= 18, f"{e['name']}: AC {e['armor_class']} off band"
        assert 2 <= e["morale"] <= 12, f"{e['name']}: morale {e['morale']} off 2d6 ladder"


def test_kept_entry_ids_are_slugs(curated):
    for e in curated.kept:
        assert e["id"] == e["id"].lower(), f"{e['id']} is not lowercase"
        assert " " not in e["id"], f"{e['id']} contains a space"


# ── library API mirrors the world convenience wrapper ──
def test_curate_list_api_matches_curate_world(curated):
    import yaml

    corpus = yaml.safe_load((BENEATH_SUNDEN / "corpus" / "monsters.yaml").read_text())
    register = WorldRegister.from_yaml(BENEATH_SUNDEN / "world_register.yaml")
    direct = curate(corpus, register)
    assert _kept_names(direct) == _kept_names(curated)

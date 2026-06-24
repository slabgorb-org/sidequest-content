"""WWN stat-ladder contract (story 158-20, AC-2 / AC-3).

These values are GROUND TRUTH, recovered from the live, validated
``beneath_sunden`` bestiary (192 entries) and its corpus join — NOT guessed
from the prose formula. The tool must reproduce the proven instance.

Key trap this suite pins (why a naive formula is wrong):
  hp == "average (4.5/HD rounded)" does NOT round consistently under any single
  Python rounding mode:
    * Python round() (banker's): round(4.5) == 4  -> would give L1 hp=4 (WRONG; live pack is 5)
    * round-half-up:             ceil(40.5-? )   -> would give L9 hp=41 (WRONG; live pack is 40)
  The canonical ladder below is what the live pack actually uses; level_to_hp
  must return exactly these.
"""

import pytest

from bestiary_curator import (
    cr_to_level,
    level_to_attack_bonus,
    level_to_hp,
    level_to_save,
)

# ── Canonical level -> hp ladder (live beneath_sunden, dominant value per level) ──
CANONICAL_HP = {1: 5, 2: 9, 3: 14, 4: 18, 5: 22, 6: 27, 7: 32, 8: 36, 9: 40, 10: 45}


@pytest.mark.parametrize("level,hp", sorted(CANONICAL_HP.items()))
def test_level_to_hp_matches_canonical_ladder(level, hp):
    assert level_to_hp(level) == hp


def test_level_to_hp_l1_is_five_not_bankers_four():
    """Regression guard: naive `round(4.5*1)` is 4 (banker's). The ladder is 5."""
    assert level_to_hp(1) == 5


def test_level_to_hp_l9_is_forty_not_half_up_fortyone():
    """Regression guard: naive round-half-up(40.5) is 41. The ladder is 40."""
    assert level_to_hp(9) == 40


def test_level_to_hp_is_monotonic_nondecreasing():
    hps = [level_to_hp(lvl) for lvl in range(1, 11)]
    assert hps == sorted(hps)
    assert len(set(hps)) == len(hps)  # strictly increasing across the band


# ── save == 15 - level//2 (live ground truth, dominant value per level) ──
CANONICAL_SAVE = {1: 15, 2: 14, 3: 14, 4: 13, 5: 13, 6: 12, 7: 12, 8: 11, 9: 11, 10: 10}


@pytest.mark.parametrize("level,save", sorted(CANONICAL_SAVE.items()))
def test_level_to_save_matches_ladder(level, save):
    assert level_to_save(level) == save


def test_level_to_save_is_fifteen_minus_half_level():
    for lvl in range(1, 11):
        assert level_to_save(lvl) == 15 - lvl // 2


# ── attack_bonus == level ──
@pytest.mark.parametrize("level", range(1, 11))
def test_level_to_attack_bonus_equals_level(level):
    assert level_to_attack_bonus(level) == level


# ── CR -> level bands (empirical, 94-creature corpus<->bestiary join) ──
# Documented anchors (bestiary banner): CR21->9, CR15->9, CR13->8, CR10->8.
EMPIRICAL_CR_LEVEL = {
    0.0: 1,
    0.125: 1,
    0.25: 1,
    0.5: 1,
    1.0: 2,
    2.0: 3,
    3.0: 3,
    4.0: 4,
    5.0: 5,
    6.0: 6,
    7.0: 6,
    8.0: 7,
    9.0: 7,
    10.0: 8,
    11.0: 8,
    12.0: 8,
    13.0: 8,
    15.0: 9,
    16.0: 9,
    17.0: 9,
    21.0: 9,
}


@pytest.mark.parametrize("cr,level", sorted(EMPIRICAL_CR_LEVEL.items()))
def test_cr_to_level_matches_empirical_bands(cr, level):
    assert cr_to_level(cr) == level


def test_cr_to_level_documented_anchors():
    """The four anchors the bestiary banner calls out explicitly."""
    assert cr_to_level(21.0) == 9  # Lich
    assert cr_to_level(15.0) == 9  # Mummy Lord
    assert cr_to_level(13.0) == 8  # Vampire
    assert cr_to_level(10.0) == 8  # Aboleth


def test_cr_to_level_low_cr_floors_at_one():
    for cr in (0.0, 0.125, 0.25, 0.5):
        assert cr_to_level(cr) == 1


def test_cr_to_level_is_monotonic_nondecreasing():
    crs = sorted(EMPIRICAL_CR_LEVEL)
    levels = [cr_to_level(cr) for cr in crs]
    assert levels == sorted(levels)


def test_cr_to_level_compresses_high_cr_into_deep_band():
    """High CR compresses into the L8-10 deep band — never exceeds the cap."""
    for cr in (21.0, 23.0, 30.0, 99.0):
        lvl = cr_to_level(cr)
        assert 8 <= lvl <= 10, f"CR {cr} -> L{lvl} escaped the deep band"

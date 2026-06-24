"""WWN/OSR stat ladder — CR-band -> level, then level -> hp/save/attack_bonus.

These are the deterministic, ruleset-tier conversions shared by every WWN world
bestiary. The values reproduce the live, validated ``beneath_sunden`` ladder
(the proven instance story 158-20 generalizes), recovered by joining the SRD
corpus CRs to the curated bestiary levels.

The hp ladder is a LOOKUP TABLE, not a formula. The prose convention is
"hp == average (4.5/HD rounded)", but no single Python rounding mode reproduces
the live values — banker's ``round(4.5)`` gives L1=4 (live is 5); round-half-up
``ceil``-style gives L9=41 (live is 40). The pack's authored ladder is mildly
irregular at the half-points, so the table itself IS the contract.
"""

from __future__ import annotations

# level -> hp, the canonical beneath_sunden ladder (L1..L10).
_HP_LADDER: dict[int, int] = {1: 5, 2: 9, 3: 14, 4: 18, 5: 22, 6: 27, 7: 32, 8: 36, 9: 40, 10: 45}

# CR upper-bound bands -> level. Empirical (94-creature corpus<->bestiary join);
# matches the four documented anchors (CR10->8, CR13->8, CR15->9, CR21->9).
# Anything above the last band compresses into the L10 deep cap.
_CR_BANDS: tuple[tuple[float, int], ...] = (
    (0.5, 1),
    (1.0, 2),
    (3.0, 3),
    (4.0, 4),
    (5.0, 5),
    (7.0, 6),
    (9.0, 7),
    (13.0, 8),
    (21.0, 9),
)
_DEEP_CAP_LEVEL = 10

_MIN_LEVEL = min(_HP_LADDER)
_MAX_LEVEL = max(_HP_LADDER)


def cr_to_level(cr: float) -> int:
    """Map a 5e Challenge Rating onto the WWN level ladder, compressing high CR
    into the L8-L10 deep band."""
    cr = float(cr)
    for upper, level in _CR_BANDS:
        if cr <= upper:
            return level
    return _DEEP_CAP_LEVEL


def level_to_hp(level: int) -> int:
    """Average hp for a WWN level, per the canonical ladder. Fails loud off-band."""
    try:
        return _HP_LADDER[level]
    except KeyError:
        raise ValueError(
            f"level {level} is off the WWN ladder (expected {_MIN_LEVEL}..{_MAX_LEVEL})"
        ) from None


def level_to_save(level: int) -> int:
    """WWN-style single save target: 15 - level//2 (ascending defence with level)."""
    if not _MIN_LEVEL <= level <= _MAX_LEVEL:
        raise ValueError(f"level {level} off-band (expected {_MIN_LEVEL}..{_MAX_LEVEL})")
    return 15 - level // 2


def level_to_attack_bonus(level: int) -> int:
    """OSR convention: attack bonus tracks Hit Dice == level."""
    if not _MIN_LEVEL <= level <= _MAX_LEVEL:
        raise ValueError(f"level {level} off-band (expected {_MIN_LEVEL}..{_MAX_LEVEL})")
    return level

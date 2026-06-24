"""The curation pipeline: SRD corpus -> curated WWN bestiary entries + drop audit.

Runs GATE 1 (genre-truth) over every corpus row, then converts each survivor
onto the WWN stat ladder. GATE 2 (tone curation — "never comic, never cute") is
NOT automated here: it is a documented human pass (see the recipe doc), because
the current ``world_register`` schema carries no biome/locomotion/role fields.

The emitted stat block is the MECHANICAL skeleton only — hp/save/attack_bonus
are ladder-exact; armor_class/morale are archetype-derived defaults the author
tunes; prose (description, abilities, damage, move) is left to the author /
narrator (158-12: deterministic materialization, narrator owns creature prose).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from .gate import GateDecision, apply_genre_truth_gate
from .ladder import cr_to_level, level_to_attack_bonus, level_to_hp, level_to_save
from .register import WorldRegister

# Mindless lineages that never check morale (Fearless, 2d6=12). Per the
# beneath_sunden banner: "12 + a Fearless ability for mindless undead / oozes /
# constructs". Authors downgrade morale for the rare cunning exception.
_FEARLESS_TYPES = frozenset({"Undead", "Ooze", "Construct"})


@dataclass(frozen=True)
class CurationResult:
    """Output of a curation run.

    ``kept`` is a list of curated stat-block dicts; ``dropped`` is the audit —
    the GateDecision for every row GATE 1 rejected (each carries its reason).
    """

    kept: list[dict]
    dropped: list[GateDecision]


def _slug(name: str) -> str:
    """A reference-page-stable id: lowercase ASCII, non-alphanumerics -> '_'."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _band(level: int) -> str:
    if level <= 2:
        return "low"
    if level <= 7:
        return "mid"
    return "deep"


def _skill(level: int) -> int:
    if level <= 3:
        return 1
    if level <= 7:
        return 2
    if level <= 9:
        return 3
    return 4


def _stat_block(decision: GateDecision, corpus_row: dict) -> dict:
    """Convert a kept corpus row into a curated WWN stat block."""
    level = cr_to_level(corpus_row["cr"])
    type_ = corpus_row.get("type", "")
    name = decision.name
    return {
        "id": _slug(name),
        "name": name,
        "level": level,
        "hp": level_to_hp(level),
        "armor_class": min(12 + level // 2, 17),
        "attack_bonus": level_to_attack_bonus(level),
        "save": level_to_save(level),
        "morale": 12 if type_ in _FEARLESS_TYPES else 8,
        "skill": _skill(level),
        "tags": [type_.lower(), _band(level)],
    }


def curate(corpus: list[dict], register: WorldRegister) -> CurationResult:
    """Gate every corpus row and convert survivors onto the WWN ladder."""
    # Fail loud (No Silent Fallbacks): an empty/None/dict-shaped corpus must not
    # silently iterate into a cryptic crash (or, for {}, silently yield nothing).
    if not isinstance(corpus, list) or not corpus:
        raise ValueError(
            f"corpus must be a non-empty list of monster rows, got {type(corpus).__name__}"
        )
    kept: list[dict] = []
    dropped: list[GateDecision] = []
    for index, row in enumerate(corpus):
        if not isinstance(row, dict):
            raise ValueError(
                f"corpus row {index} must be a mapping, got {type(row).__name__}: {row!r}"
            )
        decision = apply_genre_truth_gate(row, register)
        if decision.kept:
            kept.append(_stat_block(decision, row))
        else:
            dropped.append(decision)
    return CurationResult(kept=kept, dropped=dropped)


def curate_world(world_dir: str | Path) -> CurationResult:
    """Load ``corpus/monsters.yaml`` + ``world_register.yaml`` from a world dir
    and curate. The author-facing entry point for a single world."""
    world_dir = Path(world_dir)
    corpus = yaml.safe_load((world_dir / "corpus" / "monsters.yaml").read_text())
    register = WorldRegister.from_yaml(world_dir / "world_register.yaml")
    return curate(corpus, register)

"""WWN bestiary curator — generalizes the beneath_sunden curation pattern.

Story 158-20. Turns an SRD monster corpus into a per-world WWN bestiary by
running the world's ``world_register.yaml`` genre-truth gate (GATE 1), then
converting survivors onto the WWN/OSR stat ladder (CR -> level -> hp/save/
attack_bonus), emitting a drop audit. GATE 2 (tone) is a documented human pass.

See ``docs/bestiary-curation-recipe.md`` for the per-world contract and the
recipe the 158-21..25 world stories follow.
"""

from .curate import CurationResult, curate, curate_world
from .gate import GateDecision, apply_genre_truth_gate
from .ladder import cr_to_level, level_to_attack_bonus, level_to_hp, level_to_save
from .register import WorldRegister

__all__ = [
    "WorldRegister",
    "GateDecision",
    "apply_genre_truth_gate",
    "cr_to_level",
    "level_to_hp",
    "level_to_save",
    "level_to_attack_bonus",
    "CurationResult",
    "curate",
    "curate_world",
]

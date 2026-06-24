"""WWN bestiary curator — generalizes the beneath_sunden curation pattern.

Story 158-20. This package is the *reusable tooling* deliverable: it turns an
SRD monster corpus into a per-world WWN bestiary by running the world's
``world_register.yaml`` genre-truth gate, then converting survivors onto the
WWN/OSR stat ladder (CR -> level -> hp/save/attack_bonus), and emitting a drop
audit.

NOTE (TEA, story 158-20): this ``__init__`` is an intentional RED-phase stub.
TEA created the project scaffold + the failing test suite under ``tests/``;
Dev (GREEN phase) implements the public API the tests import:

    WorldRegister, GateDecision, CurationResult,
    apply_genre_truth_gate, curate, curate_world,
    cr_to_level, level_to_hp, level_to_save, level_to_attack_bonus

Do not add behaviour to this file as TEA — the tests must fail on missing
names until Dev implements them.
"""

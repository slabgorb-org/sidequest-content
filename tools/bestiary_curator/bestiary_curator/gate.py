"""GATE 1 — the world_register genre-truth gate.

Apply a world's ``WorldRegister`` to a single SRD corpus row and decide whether
it is admissible, recording the reason on a drop so the curation audit is
honest. Marquee rows are exempt from denial (ADR-014); reskins rename kept rows.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass

from .register import WorldRegister


@dataclass(frozen=True)
class GateDecision:
    """Outcome of GATE 1 for one corpus row.

    ``name`` is the OUTPUT name (reskinned if kept and a reskin applies; the
    original name on a drop). ``reason`` is None when kept, else a short audit
    tag like ``deny.type:Celestial`` / ``deny.tag:titan`` /
    ``deny.name_glob:*pixie*`` / ``type-not-allowed:Dragon``.
    """

    kept: bool
    reason: str | None
    name: str
    reskinned: bool


def _matching_glob(name: str, globs: list[str]) -> str | None:
    """Return the first name_glob that matches (case-insensitively), else None."""
    low = name.lower()
    for pattern in globs:
        if fnmatch.fnmatchcase(low, pattern.lower()):
            return pattern
    return None


def apply_genre_truth_gate(corpus_row: dict, register: WorldRegister) -> GateDecision:
    """Decide whether ``corpus_row`` survives GATE 1 of curation."""
    name = corpus_row["name"]
    type_ = corpus_row.get("type", "")
    tags = corpus_row.get("tags") or []

    # Marquee rows are exempt from the deny gate (Diamonds-and-Coal, ADR-014).
    if name not in register.marquee:
        if type_ in register.deny_types:
            return GateDecision(False, f"deny.type:{type_}", name, False)

        denied_tag = next((t for t in tags if t in register.deny_tags), None)
        if denied_tag is not None:
            return GateDecision(False, f"deny.tag:{denied_tag}", name, False)

        glob = _matching_glob(name, register.deny_name_globs)
        if glob is not None:
            return GateDecision(False, f"deny.name_glob:{glob}", name, False)

        if type_ not in register.allow_types:
            return GateDecision(False, f"type-not-allowed:{type_}", name, False)

    # Kept — either marquee-exempt or it passed every deny rule and is allowed.
    out_name = register.reskin.get(name, name)
    return GateDecision(True, None, out_name, out_name != name)

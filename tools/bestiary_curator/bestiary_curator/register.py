"""WorldRegister — the per-world genre-truth gate config (``world_register.yaml``).

This is GATE 1 of the two-gate curation pipeline. The register declares which
SRD creature types/tags/names are admissible for a world before any conversion
happens, plus reskins and the marquee exemption (ADR-014 Diamonds-and-Coal).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class WorldRegister:
    """Parsed ``world_register.yaml``. Field names normalize the nested
    ``deny:`` block into flat attributes for the gate."""

    register: str = ""
    allow_types: list[str] = field(default_factory=list)
    deny_types: list[str] = field(default_factory=list)
    deny_tags: list[str] = field(default_factory=list)
    deny_name_globs: list[str] = field(default_factory=list)
    reskin: dict[str, str] = field(default_factory=dict)
    marquee: list[str] = field(default_factory=list)
    humanoid_constraint: str | None = None

    @classmethod
    def from_yaml(cls, path: str | Path) -> WorldRegister:
        data = yaml.safe_load(Path(path).read_text()) or {}
        deny = data.get("deny") or {}
        return cls(
            register=data.get("register", ""),
            allow_types=list(data.get("allow_types") or []),
            deny_types=list(deny.get("types") or []),
            deny_tags=list(deny.get("tags") or []),
            deny_name_globs=list(deny.get("name_glob") or []),
            reskin=dict(data.get("reskin") or {}),
            marquee=list(data.get("marquee") or []),
            humanoid_constraint=data.get("humanoid_constraint"),
        )

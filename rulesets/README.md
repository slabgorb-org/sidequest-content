# Ruleset-tier reference content

Verbatim, player-facing SRD rules, authored **once per ruleset** and surfaced on every
pack's Rules page (`/reference/rules/<pack>`) that binds the ruleset. This is the first
content that is neither genre- nor world-tier.

- `fate/srd/*.md` — Fate Core player chapters (CC-BY 3.0, Evil Hat).
- `without_number/core/srd/*.md` — shared WN player chapters (Plan B).
- `without_number/{wwn,cwn,swn,awn}/srd/*.md` — per-game overlays; a file whose `anchor`
  matches a core file overrides it.

Each `.md` carries front-matter: `srd`, `srd_ref`, `license`, `anchor`, `title`, `order`.
All six are required (the server fails loud on a missing key). Bodies are **verbatim** —
never paraphrased — and proof-read before the `license` stamp. Attribution is rendered on
the page; it must never imply endorsement by the publisher (ADR-145 §D4a).

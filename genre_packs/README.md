# genre_packs/ — production

This is the **production** genre-pack directory. Anything in here is shipped
content, loaded by `sidequest-server` and `sidequest-daemon` at runtime.

## Consumers

- `sidequest-server` — via `SIDEQUEST_GENRE_PACKS` env var
- `sidequest-daemon` — via `SIDEQUEST_GENRE_PACKS` env var
- Orchestrator `justfile` and scripts under `orc-quest/scripts/` (image / music
  generation, playtest harness, etc.)

`SIDEQUEST_GENRE_PACKS` should point at this directory. The server enumerates
every subdirectory here and treats it as a genre; worlds that are not yet ready
set `draft: true` in their `world.yaml` to stay out of player selection.

## Readiness gate (draft → live)

In-progress packs and worlds live here like any other — there is no separate
workshopping tree (the old `genre_workshopping/` directory was retired
2026-06-03). A world stays `draft: true` until it has, at minimum:

- a complete YAML set (archetypes, axes, char_creation, beat_vocabulary,
  rules, audio.yaml — match the shape of an existing live pack)
- portraits and POI landscapes rendered and synced to R2
- audio tracks generated and indexed in `audio.yaml`
- at least one playable session run end-to-end against
  `sidequest-server` without missing-asset errors

Until then, leave `draft: true` set — the server honors it and hides the world
from selection, so partial worlds never surface to players as if finished.
Clear the flag (or omit it) only once the gate is met.

## Current packs

| Pack | Notes |
|------|-------|
| `caverns_and_claudes` | Classic dungeon crawl with meta-humor; reference pack for new authors |
| `elemental_harmony` | Martial arts / elemental magic |
| `heavy_metal` | Baroque fantasy of pacts, decay, and blood-priced magic — `evropi` + `long_foundry` |
| `mutant_wasteland` | Post-apocalyptic mutants; `flickering_reach` world is the only spoilable canon |
| `neon_dystopia` | Cyberpunk — `franchise_nations` |
| `pulp_noir` | 1930s detective / pre-war pulp — `annees_folles` |
| `space_opera` | Sci-fi space adventure |
| `spaghetti_western` | Frontier gunslinger |
| `tea_and_murder` | Cosy Edwardian BritBox murder mystery; village amateur sleuths (Glenross) |

> **Note:** `neon_dystopia`, `pulp_noir`, and `heavy_metal` were promoted /
> re-promoted 2026-05-23 with the asset gate (portraits, POI landscapes,
> generated OGG) **not yet met**. YAML loads cleanly and `*_input_params.json`
> music specs are committed, but R2-side rendered assets still need to be
> generated. (`neon_dystopia` and `pulp_noir` also still need world-tier
> `openings.yaml` authoring before they will load — see canned-openings spec
> 2026-05-01 §1; `heavy_metal` already has world openings in both worlds.)
> Until those gaps close, picking these packs may surface missing-asset paths
> or load errors. Treat as live for authoring and headless playtest; do not
> show to the playgroup until the gaps close.

## Spoiler protection

Per the project's spoiler rules, treat every world here as **unspoiled** in
chat unless the user explicitly opts in, with the sole exception of
`mutant_wasteland/flickering_reach`, which is fully spoilable.

## Editing rules

- New worlds live at `<pack>/worlds/<world>/`. Don't invent a new top-level
  layout without an ADR.
- Binary assets (images, audio) are tracked with Git LFS. Sync between
  machines via the `local` remote (see `../CLAUDE.md` → "Syncing Between
  Machines"); pulling LFS from GitHub eats the 10 GiB/month bandwidth cap.
- Schemas are validated by the server on load — see `sidequest-server` tests
  if a pack starts erroring. There is no silent-fallback path; bad YAML
  fails loudly.

# genre_packs/ — production

This is the **production** genre-pack directory. Anything in here is shipped
content, loaded by `sidequest-server` and `sidequest-daemon` at runtime.

## Consumers

- `sidequest-server` — via `SIDEQUEST_GENRE_PACKS` env var
- `sidequest-daemon` — via `SIDEQUEST_GENRE_PACKS` env var
- Orchestrator `justfile` and scripts under `orc-quest/scripts/` (image / music
  generation, playtest harness, etc.)

`SIDEQUEST_GENRE_PACKS` should point at this directory, not at
`genre_workshopping/`. The server enumerates every subdirectory here and
treats it as a selectable genre — half-built packs do not belong here.

## Promotion gate (workshop → production)

A pack moves from `genre_workshopping/` into this directory when it has, at
minimum:

- a complete YAML set (archetypes, axes, char_creation, beat_vocabulary,
  rules, audio.yaml — match the shape of an existing production pack)
- portraits and POI landscapes generated and committed under `images/`
- audio tracks generated and indexed in `audio.yaml`
- at least one playable session run end-to-end against
  `sidequest-server` without missing-asset errors

If a pack is not all of those, it lives in `../genre_workshopping/` until it
is. Do not promote partial packs — the server has no concept of "draft" and
will surface them to players as if they were finished.

## Current packs

| Pack | Notes |
|------|-------|
| `caverns_and_claudes` | Classic dungeon crawl with meta-humor; reference pack for new authors |
| `elemental_harmony` | Martial arts / elemental magic |
| `heavy_metal` | Baroque fantasy of pacts, decay, and blood-priced magic — `evropi` + `long_foundry` |
| `mutant_wasteland` | Post-apocalyptic mutants; `flickering_reach` world is the only spoilable canon |
| `neon_dystopia` | Cyberpunk — `franchise_nations` |
| `pulp_noir` | 1930s detective / pre-war pulp — `annees_folles` |
| `road_warrior` | Late-70s/early-80s vehicle subcultures sharing one port city — `the_circuit` |
| `space_opera` | Sci-fi space adventure |
| `spaghetti_western` | Frontier gunslinger |
| `tea_and_murder` | Cosy Edwardian BritBox murder mystery; village amateur sleuths (Glenross) |
| `wry_whimsy` | Golden-age literary portal fairytale; survive a dream-logic world by wit — `oz`, `wonderland`, `gulliver` (assets rendered) |

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

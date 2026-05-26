# Changelog

All notable changes to SideQuest content (genre packs, worlds, audio,
visual style configs).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Individual `pack.yaml` files carry their own per-pack version; this file
tracks the repo as a whole.

## [1.3.0] - 2026-05-26

### Added
- **elemental_harmony/shattered_accord** — world promoted from workshopping
  to production.
- **pulp_noir** + **neon_dystopia** — promoted from workshopping to
  production.
- **tea_and_murder** — `seed_tropes.yaml` with 24 short-arc Glenross hooks
  (story 22-2).
- **Reference-page chrome** — `display_font_family` and `archetype` fields
  added to every `theme.yaml` across all 10 genre packs (stories 63-3,
  63-4).
- **Music** — purchased TableTop Audio tracks wired into 6 packs, plus
  recovered tea_and_murder classical set.
- **HP / lethality (ADR-114)** — space_opera canary: weapon damage dice
  and strike-beat `damage_channel`; verdict key renamed
  `verdicts_on_zero_edge` → `verdicts_on_zero_hp`.

### Changed
- **Music** — raised ACE-Step `infer_step` 60 → 120 for heavy_metal,
  neon_dystopia, pulp_noir, and road_warrior.
- **Visual style** — genre-level suffixes now carry universal safety only;
  worlds self-complete their own style.
- **heavy_metal** — world descriptions decoupled from the pack catchphrase
  (story 62-1).
- **Pack filesystem schema** — new genre-pack schema with content migration,
  plus validator gaps closed for world files and extensions (stories 64,
  256).

### Fixed
- **flickering_reach** — opening anchors bound to cartography `region_id`.

### Removed
- CSS overlay removal (alongside POI enrichment cleanup).
- Genre-pack audio `.ogg` binaries now gitignored (R2-bound, like images).

## [1.2.0] - 2026-05-21

### Added
- **tea_and_murder** — rebrand from `victoria/` to an Edwardian cosy-crime
  pack, with the new **Glenross** Highland-village world, an 8-opening
  vocation-anchored opening bank, per-calling `class_kit` starting
  inventories (story 49-4), pack-level `weather.yaml` (story 24-2), and a
  Glenross calendar — months, days, moons, festivals, time precision
  (story 24-4).
- **tea_and_murder/glenross** — demographics baseline (cast counts,
  castle_ross household arithmetic, story 24-3), 13 Edwardian Highland NPC
  portraits + culture layers, 14 POI landscapes with image manifest, and
  Highland ACE-Step music params.
- **beneath_sunden** — new caverns_and_claudes world (Moria-as-tragedy
  descent): `world.yaml` manifest, `cartography.yaml` + `openings.yaml`
  (Ropefoot, the Dropmouth), `lore.yaml`, five RACE definitions, looks /
  affinities / special_rooms tables, a vendored BTMorton SRD corpus, a
  5-theme palette scaffold, and a world-truth gate.
- **spaghetti_western** — pack promoted from workshopping to live, with an
  1878 calendar (dust_and_lead + the_real_mccoy), `client_theme.css` for
  the theme_css transport, and expanded `the_real_mccoy` (mccoy_*) corpora.
- **caverns_and_claudes** — 4 genre-level set-piece tropes (Plan 7 §14.A).
- **Rules** — `on_intent_mismatch` + `intent_verbs` authored across 7 packs.
- **road_warrior** — restored to playable with a Rig two-pool overhaul.
- Typed `entities[]` backfill for **beneath_sunden** cartography (story
  54-5) and across all 14 **glenross** regions (story 54-4).

### Changed
- **victoria → tea_and_murder** — pack renamed; `space_opera`/
  `tea_and_murder` `pack.yaml` versions follow the rename.
- **caverns_and_claudes** — caverns_sunden deprecated in favor of
  beneath_sunden; new beneath_sunden visual anchor landed.
- **caverns_and_claudes** — Cleric/Thief signature flavor made
  pronoun-safe (2nd person).
- **caverns_sunden** — `dawn_at_the_approach` opener re-anchored at the
  Threshold Stone (not inside the vault); items catalog expanded with
  reliquaries, Crimson remnants, and consumables.
- **beneath_sunden** — fourth-wall engine vocabulary stripped from
  set-piece outcomes; corpus regenerated with sentence-case rarity and a
  fixed item-type parse.

### Fixed
- **tea_and_murder** — Lora font loaded via Google Fonts `@import` rather
  than a dead local woff2.
- **history.yaml** — trope notes + narrator log entries wrapped in the
  correct YAML shape (story 244).

### Removed
- 46 image PNGs stripped from git-LFS — R2 is the canonical home (story
  215).

## [1.1.0] - 2026-05-11

### Added
- **caverns_sunden** — full items catalog (`item_legacy_v1` named items
  plus modifier items, reliquaries for the Three Rites, crimson remnants
  from the 999 Crimson Gods, Sünden-flavored consumables).
- **caverns_sunden** — chapter→trope wiring to engage the trope engine.
- **caverns_sunden** — Sünden Square POI authoring + visual style updates.
- **coyote_star** — chapter→trope wiring (parallel content commit).
- **flickering_reach** — world-level `visual_style.yaml`.
- **caverns_and_claudes** — six ACE-Step music tracks for hamlet ambience.
- **caverns_and_claudes** — Cavern renderer revival + caverns_sunden
  world fold.
- Repo-level README + CLAUDE.md refresh (pack list, paths, ADR index).

### Changed
- **caverns_sunden/items.yaml** — header LOADER NOTE rewritten to point
  at the new server-side loader (`sidequest/genre/loader.py ::
  _load_world_items`) and the `state_transition:world_items:loaded`
  watcher event.
- **caverns_sunden/magic.yaml** — `cost_types_active` consequence comment
  expanded with Crimson Gods as the fourth Evropi import; clarifies that
  divine_favor swings AGAINST Crimson contact but not FOR it (no
  `bargained_for_v1` plugin active in Sünden).
- **caverns_and_claudes** — CON rebalance + stat_display cleanup
  (story 39-9).
- ACE-Step music params strip output-only fields on regen (per
  `feedback project_music_params_output_fields_creep`).

### Fixed
- `cavern_renderer` — ruff format + drop unused pytest imports.

### Bumped per-pack versions
- `caverns_and_claudes/pack.yaml` 1.0.0 → 1.1.0
- `space_opera/pack.yaml` 1.0.0 → 1.1.0
- `tea_and_murder/pack.yaml` 1.0.0 → 1.1.0 (was `victoria/`; pack renamed)

## [1.0.0] - prior

Initial multi-pack content baseline. Not formally tagged at the time;
recorded here for continuity. Per-pack 1.0.0 markers were set
independently per pack as each pack first shipped.

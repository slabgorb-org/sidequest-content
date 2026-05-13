# Changelog

All notable changes to SideQuest content (genre packs, worlds, audio,
visual style configs).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Individual `pack.yaml` files carry their own per-pack version; this file
tracks the repo as a whole.

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

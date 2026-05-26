# Content Authoring & Cleanup Checklist

> Generated 2026-05-26 from the genre-flavor audit. Not yet committed/triaged.

## Governing principle

- **Genre pack root** = mechanical + *genre-generic* scaffolding only: rules, generic
  role-archetype templates, tone/voice, conlang morphemes & culture naming rules,
  mechanical tropes, visual/audio style.
- **World** (`worlds/<world>/`) = *all fictional lore*: history, legends, named
  factions, named places, named cast, dated events — anything that presumes one setting.
- **A `lore.yaml` at genre root is always wrong.** Fictional lore lives in worlds.

Two fix types recur below:
- **RELOCATE** — file holds named world-fiction → move into the relevant world.
- **FOLD/DELETE** — file holds only genre-tone (no proper nouns) → fold the 1–2 keeper
  lines into `pack.yaml` (`core_vibe`/`emotional_tone`/`description`) and delete the file.
  *Every world already carries full `lore.yaml`, so most genre `lore.yaml` content is
  redundant — confirm coverage, then delete.*

---

## ⚠️ Loader blocker (found 2026-05-26) — Section A is NOT content-only

`sidequest-server/sidequest/genre/loader.py:1039` loads genre-root `lore.yaml`
via the **required** `_load_yaml` (alongside `pack.yaml`, `rules.yaml`,
`theme.yaml` at lines 1037–1040). Its docstring: *"Required; raises
GenreLoadError on any failure (file missing…). No silent fallbacks."*

**Deleting any genre-root `lore.yaml` makes that pack fail to load.** Section A
therefore requires a **paired `loader.py` change** first — switch line 1039 to
`_load_yaml_optional` (or drop the genre-root lore load entirely and rely on the
per-world `lore.yaml`). That is a server change and must wait until
`sidequest-server` is off `feat/postgres-substrate` (ADR-115 TG2). Until then,
genre-root `lore.yaml` files stay in place; the most we can do content-side is
ensure they carry **no named world-fiction** (they are already tone-only per the
table below).

## A. Genre-root `lore.yaml` — remove from all 10 packs

| Pack | Genre lore.yaml | Content | Action |
|---|---|---|---|
| heavy_metal | 193 ln | **Named fiction** — six feeding cults (First Feeders/Unfed/Refusers), named prehistory, pact cosmology. Both worlds (evropi 563, long_foundry 119) already carry full lore. | **RELOCATE/DELETE** — confirm each world owns its faction lore, then delete genre copy. Decide first: do evropi + long_foundry share one setting, or each own its cults? |
| space_opera | 68 ln | **Named fiction** — Hegemony, Rim Confederacy, Guilds, Void Clans + jump-point geography. Worlds specialize (coyote_star → Clan Moana-Teru). | **RELOCATE/DELETE** — same shared-setting decision (aureate_span + coyote_star), then delete. |
| caverns_and_claudes | 93→61 | Keeper/Maw dungeon-mythos. Borderline: pack conceit, no named place. | **DECIDE** — if it's the genre conceit, encode as tone in `pack.yaml`; else delete. |
| neon_dystopia | 23 ln | Genre-philosophy, no proper nouns (*"humanity measured in percentages"*). | **FOLD→pack.yaml + DELETE** |
| pulp_noir | 20 ln | Genre-philosophy, no proper nouns (*"law and crime is a gentleman's agreement"*). | **FOLD→pack.yaml + DELETE** |
| road_warrior | 20 ln | Pure tone (*"the rig as altar"*). | **FOLD→pack.yaml + DELETE** |
| spaghetti_western | 62 ln | Genre-philosophy, no world locations (*"the bullet does not care"*). | **FOLD→pack.yaml + DELETE** |
| tea_and_murder | 38 ln | Genre-philosophy (*"every great house a world unto itself"*). | **FOLD→pack.yaml + DELETE** |
| mutant_wasteland | 11 ln | Thin genre-primer, no named fiction. | **FOLD→pack.yaml + DELETE** |
| elemental_harmony | 13 ln | Near-stub (`world_name: ""`, `geography: ""`). | **DELETE** (vestigial) |

- [ ] heavy_metal — resolve shared-setting question, relocate/delete genre `lore.yaml`
- [ ] space_opera — resolve shared-setting question, relocate/delete genre `lore.yaml`
- [ ] caverns_and_claudes — decide Keeper/Maw home, remove genre `lore.yaml`
- [ ] neon_dystopia / pulp_noir / road_warrior / spaghetti_western / tea_and_murder / mutant_wasteland — fold tone into `pack.yaml`, delete genre `lore.yaml`
- [ ] elemental_harmony — delete stub genre `lore.yaml`

## B. Other genre-root files smuggling world-fiction

- [ ] **tea_and_murder/seed_tropes.yaml** — 20 hooks name glenross cast (Old Tam, Mrs. Buchan,
      Sgt. Macrae, St. Maelrubha's). **RELOCATE to `worlds/glenross/`.** Author generic
      genre-level seed tropes only if a genre-level fallback is wanted.
      ⚠️ **Verify first (2026-05-26):** genre-root load is *optional*
      (`loader.py:1076` `_load_yaml_raw_optional`), so deleting the genre copy
      won't break load — **but** it's unconfirmed whether the *world* loader
      reads `worlds/<world>/seed_tropes.yaml`. If it doesn't, relocating there
      silently drops the hooks (a silent-fallback trap). Trace the world-loader
      path before moving.
- [ ] **tea_and_murder/weather.yaml** — comments reference glenross-specific legends.
      Strip the glenross refs (also violates no-comments rule); keep generic weather mechanics.
- [ ] **spaghetti_western/calendar.yaml** — `texture_by_world:` blocks name Sangre Territory
      vs Pittsburgh. Either accept as a deliberate cross-world index, or push texture into worlds.
- [ ] **spaghetti_western/history.yaml** — half scenario-design scaffolding (session-range
      gates) rather than genre flavor. Decide: keep as campaign-arc template or move.
- [ ] **tea_and_murder/history.yaml** — Victorian dated events (genre-era grounding, milder).
      Keep as genre-era reference or move; has `world_name: ""` cruft to strip.

## C. World authoring HOLES — new content needed

- [ ] **space_opera/aureate_span — `archetypes.yaml` MISSING.** Has `archetype_funnels.yaml`
      but no archetype definitions (coyote_star has 288 ln). Either author world archetypes,
      or confirm it intends to fall back to the 8 genre-generic archetypes.
- [ ] **tea_and_murder/blackthorn_moor — `openings.yaml` MISSING.** Zero openings (glenross
      has 1451 ln). **Blocks session start** — highest-priority hole.
- [ ] **tea_and_murder/blackthorn_moor — `cultures/` empty.** glenross has 2; author or confirm
      blackthorn reuses genre cultures.
- [ ] blackthorn_moor reads as a half-built second world overall — needs an authoring pass
      to parity with glenross before it's playable.

## D. Hygiene (no-comments-in-content rule)

- [x] **neon_dystopia/cultures.yaml** — comments stripped (2026-05-26, parse-verified).
      **Surfaced load-bearing note** (relocate to a corpus/naming validator, do not lose):
      naming should lean on real cultural names with cyberpunk handles layered on top,
      not pure Markov generation (was a TODO at the file head).
- [x] **pulp_noir/cultures.yaml** — comments stripped (2026-05-26, parse-verified).
      Surfaced note: pulp_noir uses static `names_file:` lists, **no Markov** — already
      encoded in the data slots, so the comment was redundant.
- [x] **tea_and_murder/weather.yaml** — comments stripped (2026-05-26, 307→205 lines,
      `yaml.safe_load` proven identical before/after). The bulk were glenross world-fiction
      (the Section-B leak — now gone from genre root) + per-season flavor. **Surfaced
      load-bearing rules that were ONLY in comments — these need a real home (world-grounding
      validator), they are no longer documented anywhere:**
        - **Season-id invariant:** season ids are the Edwardian four (spring/summer/autumn/
          winter); the future `glenross/calendar.yaml` (story 24-4) MUST reuse the same ids
          or prompt-zone alignment fails. → wants a cross-file validator.
        - Schema: `docs/schemas/world-grounding/weather.schema.json` (pack level), PRD §1.1
          (Epic 24, Phase 1).
        - Units: `temp_range` values are degrees Celsius (genre default per schema).
- [ ] Sweep other genre-root YAML for inline comments while doing A/B.

## E. Genre-generic scaffolding — decisions

- [ ] **space_opera has no genre-level `openings.yaml`** (road_warrior/neon/pulp/spaghetti/
      heavy_metal do). Decide whether genre packs should carry generic situation openings as a
      fallback, or openings are strictly world-level. Apply the answer consistently across packs.
- [ ] Confirm the model pack: **heavy_metal** already empties genre `cultures.yaml`/`archetypes.yaml`
      to `[]` and lets worlds carry them — if that's the target architecture, the other packs'
      genre-level archetypes/cultures need re-checking that they're truly *generic* templates,
      not world-flavored.

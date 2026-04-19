# Evropi — Per-Character Progression Trees (Post-Epic-39 Content)

**Status:** Drafts, lifted verbatim when Epic 39 lands. Each file is a world-level per-character milestone-grant YAML — a second tier layered *on top of* the genre-level `progression.yaml` affinity mechanical_effects that Margaret ratified (see `sidequest-content/genre_packs/heavy_metal/_drafts/edge-advancement-content.md` §2).

**Architecture:**
- **Base layer:** `heavy_metal/progression.yaml` — affinity tier mechanical_effects every heavy_metal character receives when crossing thresholds. Identical across worlds.
- **This layer:** `worlds/evropi/character-progression/{slug}.yaml` — per-character milestone grants, unlocked by specific in-world triggers, keyed to that character's biography. These are *additional* `AdvancementEffect` entries layered on top of the baseline affinity effects.

**Author:** GM (Hawkeye), 2026-04-18
**Consumer:** Story 39-5 adds the `milestone-grant path` that loads these files. Schema proposed below.

---

## Proposed schema (story 39-5 wiring target)

```yaml
character:
  save_id: string                    # matches ~/.sidequest/saves/{genre}/{world}/{save_id}/
  name: string
  race: string
  class: string
  affinity_emphasis:                 # narrator hint only — drives flavor, not mechanics
    primary: [affinity_name, ...]
    secondary: [affinity_name, ...]
    rare: [affinity_name, ...]
    absent: [affinity_name, ...]

trunk:                               # granted at L1, persistent
  id: snake_case_id
  label: "Human-readable title"
  narration_hint: "Prose for the narrator — load as high-priority KnownFact."
  effects:
    - { type: advancement_effect_type, ... }

paths:
  - id: snake_case_id
    label: "Path name"
    flavor: "One-sentence description."
    nodes:
      - tier: 1 | 2 | 3
        id: snake_case_id
        label: "Node name"
        milestone_category: oath | debt | ruin | revelation | reckoning
        grant_trigger:                # what causes this to unlock
          condition: string           # e.g. "affinity:Lore:tier:1" or "milestone:revelation:3"
        narration_hint: "Prose."
        effects:
          - { type: ..., ... }        # typed AdvancementEffect enum
          # OR
        effects: []                   # TODO ADR-082+ — <reason>, flavor preserved

capstones:
  unlock_condition: "any path tier 2 reached"
  choose: 1
  options:
    - id: snake_case_id
      label: "Capstone name"
      narration_hint: "Prose."
      permanent_effect: "Narrator-honored permanent character change."
      effects:
        - { type: ..., ... }
```

## `AdvancementEffect` vocabulary (day-1 enum, per ADR-078 amended)

| Type | Fields | Use for |
|---|---|---|
| `edge_max_bonus` | `amount: i32` | More composure capacity |
| `beat_discount` | `beat_id: string, edge_delta_mod?: i32, resource_mod?: map<str,i32>` | Make a specific beat cheaper in Edge or push-currency |
| `leverage_bonus` | `beat_id: string, target_edge_delta_mod: i32` | Strip more Edge from opponents on a specific beat |
| `edge_recovery` | `trigger: { type: on_resolution \| on_beat_success [+while_strained] }, amount: i32` | Refill Edge on specific conditions |
| `lore_reveal_bonus` | `scope: enum` | Narrator must reveal one true fact on first encounter |

## ADR-082+ deferred variants

Nodes that need `ally_beat_discount`, `between_confrontations_action`, `ally_edge_grant`, or `edge_threshold_delay` ship as `effects: []  # TODO ADR-082+ — <reason>` with labels and narration_hints fully authored. Same pattern as heavy_metal/progression.yaml Craft/Lore T2–T3.

## Files in this folder

- `rux.yaml` — Kobold Rogue, Tismenni servant-line
- `prot_thokk.yaml` — Half-Orc Fighter, Cheeney's guardian (consumes ADR-081 `ally_edge_intercept`)
- `hant.yaml` — Antman Bard, pheromone-composer (heavy ADR-082+ dependency for T2/T3 ally variants)
- `ludzo.yaml` — Human Rogue, Zkęd exile (test sandbox — starting_kit inherits rux)
- `pumblestone_sweedlewit.yaml` — Gnome Wizard, forgetful sage
- `th_rook.yaml` — Pakook`rook Warlock, reniksnad-dependent (consumes ADR-081 `conditional_effect_gating`; character_resources: reniksnad)

## Scope tally

5 playgroup characters + 1 test sandbox = 6 files.

**Starting kits:** 3 grants per character. All day-1 enum effects EXCEPT:
- Prot'Thokk's *Lil' Sebastian Stands* uses ADR-081 `ally_edge_intercept`
- Th`rook's *The Dose Helps* uses ADR-081 `conditional_effect_gating`
- Th`rook's path *The Body Keeps Its Own Ledger* (tier 2) uses ADR-081 `conditional_effect_gating` (future progression, not day-one)

**Progression content (trunk + paths + capstones):** 13 nodes per character = 65 additional content entries. Roughly half land on day-1 enum; roughly half ship as ADR-082+ stubs with preserved labels and narration_hints.

**Character resources:** Th`rook has a character-scoped `reniksnad` ResourcePool (new schema extension alongside the genre-level Voice/Flesh/Ledger).

**Sunday deployment:** All five playgroup characters run under GM fiat via `../sunday-progression.md`. Post-Epic-39 story 5: starting kits and character resources hydrate at chargen.

(Aberu Kisu retired 2026-04-18.)

— Hawkeye, 2026-04-18

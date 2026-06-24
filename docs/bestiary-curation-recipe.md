# WWN Bestiary-Curation Recipe — the per-world contract

> Story 158-20. Generalizes the proven `beneath_sunden` curation into a reusable
> **per-world contract** plus tooling (`tools/bestiary_curator/`). The
> per-world stories **158-21..25** (barsoom, evropi, long_foundry,
> burning_peace, shattered_accord) follow this recipe.

A world that binds a Without-Number ruleset (WWN/CWN/SWN, per ADR-142/143) owns
its own **cast and catalog** (ADR-140): the genre is the rulebook, the world is
the bestiary. This recipe is how you turn a raw SRD monster list into a curated,
setting-true, mechanically-valid world bestiary **without touching engine code**.

## The four stages

```
  corpus/monsters.yaml            world_register.yaml
   (SRD source rows)         (GATE 1 — genre-truth gate)
          │                          │
          └──────────►  GATE 1  ◄────┘     deterministic — tools/bestiary_curator
                          │
                          ▼
                       GATE 2  ── tone curation (HUMAN pass — see below)
                          │
                          ▼
                   WWN stat ladder        deterministic — tools/bestiary_curator
                   (CR → level → stats)
                          │
                          ▼
                    bestiary.yaml
                          │
                          ▼
                    pack-validate         load_genre_pack + cliché-judge
```

### Stage 0 — `corpus/monsters.yaml` (the SRD source)

Drop the handed-in SRD roster at
`genre_packs/<genre>/worlds/<world>/corpus/monsters.yaml`. Each row:

```yaml
- name: Aboleth
  size: Large
  type: Aberration        # 5e creature type — the GATE 1 allow/deny key
  tags: []                # e.g. [titan], [shapechanger]
  alignment: lawful evil
  cr: 10.0                # Challenge Rating — the stat-ladder key
  xp: 5900
  source: SRD 5.1
```

> **Source ≠ the D&D SRD for every world.** For settings like ERB's Barsoom or
> a wuxia/elemental world, the SRD is largely *inapplicable* — the corpus is the
> **setting's own fauna** (tharks, banths, calots; spirits, cultivators,
> dao-beasts) authored onto the same row shape, with a plausible `type`/`cr`.
> See 158-21 / 158-24.

### Stage 1 — GATE 1: the `world_register.yaml` genre-truth gate (deterministic)

`world_register.yaml` is the world's **fidelity statement** — applied *before*
any stat conversion. A denied row is removed from the bestiary entirely.

```yaml
# Fidelity statement: tone + a gravity floor. Prose, for the author + reviewer.
register: "Grave, lethal, Moria-as-tragedy. Gravity >= 0.85. No winking."

allow_types: [Undead, Aberration, Ooze, Monstrosity, Construct, Giant, Humanoid, Beast]
deny:
  types: [Celestial, Fey]                       # whole 5e types this world refuses
  tags:  [titan, metallic, angel, genie]        # tag-level vetoes (Kraken/Tarrasque carry `titan`)
  name_glob: ["*modron*", "*pixie*", "*mephit*"] # case-insensitive fnmatch on name
humanoid_constraint: "Humanoid only as grave cultists / the delved-too-deep — never townsfolk-tone."
reskin:
  "Gray Ooze": "The Seep"                        # keep the stats, rename to the world
marquee: ["Lich", "Mummy Lord", "Vampire"]       # exempt from denial (ADR-014 Diamonds-and-Coal)
```

GATE 1 decision order (see `bestiary_curator/gate.py`):

1. **marquee** → kept, exempt from every deny rule below (Diamonds-and-Coal).
2. `deny.types` → dropped (`deny.type:<T>`).
3. `deny.tags` → dropped (`deny.tag:<t>`).
4. `deny.name_glob` → dropped, case-insensitively (`deny.name_glob:<glob>`).
5. type not in `allow_types` → dropped (`type-not-allowed:<T>`).
6. otherwise kept; `reskin` renames the kept row.

### Stage 2 — GATE 2: tone curation (HUMAN pass — *not* automated)

GATE 1 is type/tag/name algebra. GATE 2 is **judgment** — "Moria-as-tragedy,
never comic, never cute" — and it is **deliberately not automated**, because the
`world_register` schema carries no biome/locomotion/role fields to encode it.
The author hand-removes the survivors that pass GATE 1 but break tone, e.g.:

- surface fauna in a lightless mine (camels, sharks, dinosaurs),
- dedicated flyers where the fiction has no sky (Roc, Griffon, Manticore),
- comic/joke lineages (modron drones, whimsical homebrew),
- wrong-biome humanoids.

Record every GATE 2 drop in the bestiary banner (see the audit template below).
On the `beneath_sunden` reference, GATE 1 keeps **208**; GATE 2 + dedup trims to
the shipped **192**.

### Stage 3 — the WWN stat ladder (deterministic)

Survivors convert onto the ruleset's OSR stat ladder. For **WWN**, recovered
ground-truth from the live `beneath_sunden` ladder:

| level | hp | save (`15 − level//2`) | attack_bonus (`== level`) | skill | band |
|------:|---:|---:|---:|---:|------|
| 1 | 5 | 15 | 1 | 1 | low |
| 2 | 9 | 14 | 2 | 1 | low |
| 3 | 14 | 14 | 3 | 1 | mid |
| 4 | 18 | 13 | 4 | 2 | mid |
| 5 | 22 | 13 | 5 | 2 | mid |
| 6 | 27 | 12 | 6 | 2 | mid |
| 7 | 32 | 12 | 7 | 2 | mid |
| 8 | 36 | 11 | 8 | 3 | deep |
| 9 | 40 | 11 | 9 | 3 | deep |
| 10 | 45 | 10 | 10 | 4 | deep |

> **hp is a table, not a formula.** The prose convention is "average
> (4.5/HD rounded)", but the authored ladder is irregular at the half-points
> (L1=5 not banker's-4; L9=40 not half-up-41). `level_to_hp` reproduces the
> table; do not "fix" it to a formula.

**CR → level** compresses high CR into the L8-10 deep band:

| CR | ≤0.5 | 1 | 2-3 | 4 | 5 | 6-7 | 8-9 | 10-13 | 14-21 | >21 |
|----|------|---|-----|---|---|-----|-----|-------|-------|-----|
| level | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |

Anchors (bestiary banner): Aboleth CR10→L8, Vampire CR13→L8, Mummy Lord CR15→L9,
Lich CR21→L9.

`armor_class` (12-17 by armor archetype) and `morale` (2d6 ladder; **12 =
Fearless** for mindless undead/oozes/constructs) are **archetype-driven**, not
level functions. The tool emits sane defaults (AC `min(12+level//2,17)`; morale
12 for Undead/Ooze/Construct else 8); the author tunes them. Prose
(`description`, `abilities`, `damage`, `move`) is left to the author / narrator
(158-12: deterministic materialization, narrator owns creature prose).

> **Other rulesets:** CWN/SWN share the OSR shape but may diff the HD die / save
> model. When a 158-2x world binds a non-WWN ruleset, parameterize the ladder
> for that ruleset rather than reusing the WWN table verbatim.

### Stage 4 — pack-validate

The curated `bestiary.yaml` must pass the **real wiring gate**:

```bash
# strong gate — the loader, not just `validate pack`
uv run python -c "from sidequest.genre.loader import load_genre_pack; \
  load_genre_pack('genre_packs/<genre>')"     # from sidequest-server
```

…and a **cliché-judge** pass on the curated roster. `validate pack` reporting
0/0 is NOT proof a pack loads (see `MEMORY` / world-builder notes).

## The tooling — `tools/bestiary_curator/`

Deterministic GATE 1 + ladder + audit. Library + CLI; no LLM.

```bash
# from the sidequest-content repo root
python -m bestiary_curator genre_packs/<genre>/worlds/<world>            # entries -> stdout
python -m bestiary_curator genre_packs/<genre>/worlds/<world> --out b.yaml
#   stderr: "# GATE 1: kept N, dropped M" + one "DROP <name>: <reason>" per drop
```

Library API (`from bestiary_curator import ...`):

| symbol | purpose |
|--------|---------|
| `WorldRegister.from_yaml(path)` | parse `world_register.yaml` |
| `apply_genre_truth_gate(row, reg) -> GateDecision` | GATE 1 for one row (`.kept/.reason/.name/.reskinned`) |
| `cr_to_level / level_to_hp / level_to_save / level_to_attack_bonus` | the WWN stat ladder |
| `curate(corpus, reg) -> CurationResult` | gate + convert a corpus (`.kept`, `.dropped`) |
| `curate_world(world_dir) -> CurationResult` | load a world's corpus + register and curate |

Run its tests: `cd tools/bestiary_curator && uv run --extra dev pytest`.

## Per-world audit-trail template

Every world's `bestiary.yaml` banner must record its curation provenance so the
choices are legible to the next author / reviewer:

```text
# ── <World> WWN bestiary — curation provenance ───────────────────────
#  SOURCE: <SRD 5.1 | the setting itself (Barsoom / wuxia / …)>, <N> rows.
#  GATE 1 (world_register genre-truth): dropped <…> by type / <…> by tag /
#    <…> by name_glob — <K1> culled.   [tool: bestiary_curator]
#  GATE 2 (tone — "<register line>"): hand-dropped <…> — <K2> culled.
#  RESKIN: "<SRD name>" -> "<world name>" (×R).
#  MARQUEE (Diamonds-and-Coal, exempt): <names>.
#  CONVERSION: WWN ladder (CR→level deep-cap; hp table; save 15−level//2;
#    attack_bonus == level). AC/morale archetype-tuned by hand.
#  VALIDATION: load_genre_pack PASS; cliché-judge PASS.
# ─────────────────────────────────────────────────────────────────────
```

## Per-world checklist (158-21..25)

1. Author/drop `corpus/monsters.yaml` (setting-true source).
2. Author `world_register.yaml` (allow/deny/reskin/marquee + fidelity line).
3. `python -m bestiary_curator …` → curated GATE 1 + ladder skeleton.
4. **GATE 2 by hand**: trim tone-breakers; tune AC/morale; add prose/marquee plates.
5. Write the audit-trail banner (template above).
6. `load_genre_pack` + cliché-judge → green.

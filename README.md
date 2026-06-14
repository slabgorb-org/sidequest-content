# sidequest-content

The single source of truth for SideQuest **genre-pack specs** — YAML
configuration, generation parameters, world data, and culture corpora. Read by
both `sidequest-server` (Python game engine) and `sidequest-daemon` (Python
media services) via the `SIDEQUEST_GENRE_PACKS` environment variable.

> **Rendered media assets (images AND audio) are NOT canonical in this repo.**
> They are canonical in R2 (`cdn.slabgorb.com`), and the authoritative index of
> what exists is **`r2_manifest.json`** at the repo root (a full bucket scan:
> `key`, `md5`, `size_bytes`, `uploaded_at` per object). What git holds is the
> *spec* — the prompts, manifests, and generation parameters that regenerate a
> binary — not the binary itself. When the local workspace and R2 disagree on a
> rendered asset, **R2 wins**; rebuild the index with
> `scripts/r2_manifest_from_bucket.py`.
>
> - **Audio:** per-track ACE-Step generation parameters (`*_input_params.json`
>   under `genre_packs/<pack>/audio/music/`) are the canonical regeneration
>   spec — see [ADR-095](../orc-quest/docs/adr/095-daemon-music-tier-via-ace-step.md).
>   The OGG lives in R2.
> - **Images:** `portrait_manifest.yaml`, POI yaml, and `visual_style.yaml`
>   prompt text are the canonical spec. The rendered PNG lives in R2, indexed
>   by `r2_manifest.json`.

## Genre packs (live)

| Pack | Theme | Worlds present |
|------|-------|----------------|
| `caverns_and_claudes` | Classic dungeon crawl (meta-humor on D&D tropes) | `beneath_sunden` (single-shaft procedural megadungeon, ADR-106; surface anchor authored, deep is runtime) |
| `elemental_harmony` | Martial arts / elemental magic | `burning_peace`, `shattered_accord` |
| `heavy_metal` | Baroque fantasy of pacts, decay, and blood-priced magic | `evropi`, `long_foundry`, `barsoom` (WWN ruleset; portraits still rendering) |
| `mutant_wasteland` | Post-apocalyptic mutants | `flickering_reach` (fully spoilable), `seaboard_of_saints` |
| `neon_dystopia` | Cyberpunk | `franchise_nations` |
| `pulp_noir` | 1930s detective / pre-war pulp | `annees_folles` |
| `road_warrior` | Late-70s / early-80s vehicle subcultures sharing one port city (bōsōzoku, mods, lowriders, dekotora, raggare, &c.) | `the_circuit` |
| `space_opera` | Sci-fi space adventure | `aureate_span` (baroque corona megastation), `coyote_star`, `perseus_cloud` |
| `spaghetti_western` | Morally ambiguous anti-heroes — Leone/Corbucci/Kurosawa. Standoff as ritual, betrayal as inevitability. | `dust_and_lead` (Sangre Territory border town), `five_points` (1850s NYC Sixth Ward), `the_real_mccoy` (1878 industrial Pittsburgh) |
| `tea_and_murder` | Cosy Edwardian (1901-1914) BritBox-register murder mystery; village amateur sleuths, episodic mysteries | `glenross`, `blackthorn_moor` |
| `wry_whimsy` | Golden-age literary portal fairytale; a sensible traveler in a dream-logic Secondary World survives by wit over force, episodic with an undertow of menace | `oz`, `wonderland`, `gulliver` (light-to-savage gradient; assets rendered) |

Each pack contains YAML configs (archetypes, tropes, rules, encounters,
factions, OCEAN profiles, conlang morphemes, audio cues, visual style), and
asset directories for portraits, POI landscapes, and music params.

All eleven packs above have a `pack.yaml` and are loaded at runtime. Worlds
default to live; `draft: true` in a world's `world.yaml` hides it from
selection until its asset gate (portraits + POI landscapes rendered to R2) is
met. There are currently no draft worlds — all worlds are live.

In-progress packs and worlds live in `genre_packs/` like any other and use
`draft: true` (above) to stay hidden from selection until their asset gate is
met. The old `genre_workshopping/` staging tree was retired on 2026-06-03 when
`low_fantasy` was removed — `draft` status replaces it.

## Layout

```
sidequest-content/
├── genre_packs/                  # Live, wired packs (loaded at runtime)
│   ├── <pack>/
│   │   ├── pack.yaml             # Pack metadata + base archetypes/tropes/rules
│   │   ├── audio/
│   │   │   ├── music/            # Track folders with *_input_params.json (ADR-095)
│   │   │   └── sfx/              # Audio cues
│   │   ├── visual_style.yaml     # Z-Image prompt style (ADR-086)
│   │   ├── portraits/            # Character portrait images
│   │   ├── pois/                 # POI landscape images
│   │   └── worlds/<world>/       # World-specific overrides
│   │       ├── world.yaml
│   │       ├── world.cartography.yaml
│   │       └── ...
├── corpus/                       # Conlang word lists per culture (ADR-091)
├── docs/                         # Authoring checklist + Z-Image prompting guide
├── archetypes_base.yaml          # Shared archetype scaffolding
├── npc_traits.yaml               # Cross-pack trait pool
├── pack_schema.yaml              # Genre-pack schema (validation target)
├── r2_manifest.json              # Index of record for R2 assets (full bucket scan)
├── tools/                        # Pack authoring tooling
├── runs/                         # Local generation outputs (gitignored)
├── CHANGELOG.md                  # Content change log
├── PROMPTING_Z_IMAGE.md          # Z-Image prompting guide (no negatives)
└── SOUL.md                       # In-world design doctrine
```

## Consumers

- **`sidequest-server`** — Reads packs at boot via `SIDEQUEST_GENRE_PACKS`. Lazy-binds genre + world per session (ADR-004).
- **`sidequest-daemon`** — Reads `visual_style.yaml`, `audio/music/*_input_params.json`, and prompts/recipes for image and music generation.
- **Orchestrator `scripts/`** — `generate_poi_images.py`, `generate_music.py`, world-builder tools.

## Asset taxonomy (ADR-086)

Three image composition tiers, each with its own visual rules:

- **Portrait** — Character. Single subject, tight framing, identity-consistent.
- **POI landscape** — Location. Establishing shot, no subject foreground.
- **Illustration** — Scene / handout. Multi-subject, narrative composition.

Tactical maps are pre-rendered (ADR-096, cavern renderer revival), not generated per turn.

## Cultures and naming (ADR-091)

`corpus/<culture>/` holds curated word lists driving Markov name generation
per culture binding. Adding a new culture means: write the corpus, bind it in
the pack's `cultures.yaml`, and validate via `sidequest namegen`.

## Audio assets

- **In repo:** `*_input_params.json` per track — the canonical ACE-Step generation spec.
- **In R2 (`cdn.slabgorb.com`):** Rendered OGG files served to clients.
- Music is generated on operator command: `python scripts/generate_music.py --genre <pack>` from the orchestrator (ADR-095). Re-running is idempotent and safe to leave durable.

## Image assets (R2-canonical)

Rendered images are **canonical in R2**, indexed by `r2_manifest.json` — the
same model as audio. Git holds only the spec (`portrait_manifest.yaml`, POI
yaml, `visual_style.yaml` prompt text). Render scripts
(`scripts/generate_portrait_images.py`, `generate_poi_images.py`,
`generate_creature_images.py`) write PNGs into the local workspace;
`scripts/r2_sync_packs.py` uploads them to R2; `scripts/r2_manifest_from_bucket.py`
rebuilds the index.

**Do not treat local PNGs as the source of truth, and do not commit fresh ones.**
The `.gitattributes` `*.png filter=lfs` rules and a residue of historical
LFS-committed PNGs predate the R2 migration — they are legacy, not canonical.
Where a local copy and R2 disagree, R2 wins. Multiple local folder conventions
(`<pack>/images/<type>/`, `<pack>/assets/images/<type>/`,
`<pack>/worlds/<world>/assets/<type>/`) exist only as historical render-output
drift; the canonical location of any asset is whatever key holds it in
`r2_manifest.json`. (The only LFS binaries that legitimately stay in git are
`.safetensors` LoRA weights and the cavern-renderer test fixtures.)

> **Do not pull from GitHub to sync between local repos** — it eats LFS bandwidth (10 GiB/month limit on GitHub Pro).

Each clone has a `local` remote pointing to the other machine's copy:

```bash
git pull local main    # Sync from the other local clone (no GitHub bandwidth)
git push origin main   # Only when you want a remote backup
```

### First-time setup on a new machine

```bash
git clone --no-hardlinks /path/to/existing/sidequest-content /path/to/new/sidequest-content
cd /path/to/new/sidequest-content
git remote set-url origin git@github.com:slabgorb-org/sidequest-content.git
git remote add local /path/to/existing/sidequest-content
```

## Validation

```bash
# From sidequest-server:
uv run python -m sidequest.cli.validate /path/to/genre_packs/<pack>
```

## Spoiler protection

- **Fully spoilable:** `mutant_wasteland/flickering_reach` only
- **Fully unspoiled:** Everything else

When working in unspoiled packs, treat scenario beats, clue graphs, NPC
identities, and world secrets as opaque — read the schema, not the answer.

## Related repos

- [sidequest](https://github.com/slabgorb-org/sidequest) — Orchestrator, ADRs
- [sidequest-server](https://github.com/slabgorb-org/sidequest-server) — Python FastAPI backend
- [sidequest-daemon](https://github.com/slabgorb-org/sidequest-daemon) — Python media services
- [sidequest-ui](https://github.com/slabgorb-org/sidequest-ui) — React client
- [sidequest-composer](https://github.com/slabgorb-org/sidequest-composer) — Notation → rights-free audio (offline tool)
- [sidequest-understudy](https://github.com/slabgorb-org/sidequest-understudy) — Naive simulated-player playtest client

# sidequest-content

The single source of truth for SideQuest **genre packs** — YAML configuration,
audio, images, world data, and culture corpora. Read by both
`sidequest-server` (Python game engine) and `sidequest-daemon` (Python media
services) via the `SIDEQUEST_GENRE_PACKS` environment variable.

> **Audio assets are NOT in this repo.** They live in R2 (`cdn.slabgorb.com`).
> Per-track ACE-Step generation parameters (`*_input_params.json` under
> `genre_packs/<pack>/audio/music/`) ARE in this repo and are the canonical
> regeneration spec — see [ADR-095](../orc-quest/docs/adr/095-daemon-music-tier-via-ace-step.md).

## Genre packs (live)

| Pack | Theme | Worlds present |
|------|-------|----------------|
| `caverns_and_claudes` | Classic dungeon crawl (meta-humor on D&D tropes) | `beneath_sunden` (single-shaft procedural megadungeon, ADR-106; surface anchor authored, deep is runtime) |
| `elemental_harmony` | Martial arts / elemental magic | `burning_peace`, `shattered_accord` |
| `heavy_metal` | Baroque fantasy of pacts, decay, and blood-priced magic | `evropi`, `long_foundry` (portraits pending render) |
| `mutant_wasteland` | Post-apocalyptic mutants | `flickering_reach` (fully spoilable) |
| `neon_dystopia` | Cyberpunk | `franchise_nations` |
| `pulp_noir` | 1930s detective / pre-war pulp | `annees_folles` |
| `road_warrior` | Late-70s / early-80s vehicle subcultures sharing one port city (bōsōzoku, mods, lowriders, dekotora, raggare, &c.) | `the_circuit` |
| `space_opera` | Sci-fi space adventure | `aureate_span` (baroque corona megastation), `coyote_star`, `perseus_cloud` |
| `spaghetti_western` | Morally ambiguous anti-heroes — Leone/Corbucci/Kurosawa. Standoff as ritual, betrayal as inevitability. | `dust_and_lead` (Sangre Territory border town), `five_points` (1850s NYC Sixth Ward), `the_real_mccoy` (1878 industrial Pittsburgh) |
| `tea_and_murder` | Cosy Edwardian (1901-1914) BritBox-register murder mystery; village amateur sleuths, episodic mysteries | `glenross`, `blackthorn_moor` (draft) |

Each pack contains YAML configs (archetypes, tropes, rules, encounters,
factions, OCEAN profiles, conlang morphemes, audio cues, visual style), and
asset directories for portraits, POI landscapes, and music params.

All ten packs above have a `pack.yaml` and are loaded at runtime. Worlds
default to live; `draft: true` in a world's `world.yaml` hides it from
selection until its asset gate (portraits + POI landscapes rendered to R2) is
met. `blackthorn_moor` is currently the only draft world.

Stub / workshopping packs not yet wired into runtime live under
`genre_workshopping/` (caverns_sunden — deprecated three-sins hub superseded
by `beneath_sunden`; low_fantasy at various levels of completeness).
`genre_workshopping/{elemental_harmony,space_opera,tea_and_murder}/worlds/`
hold in-progress alternate worlds for the live packs of the same name.

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
├── archetypes_base.yaml          # Shared archetype scaffolding
├── npc_traits.yaml               # Cross-pack trait pool
├── tools/                        # Pack authoring tooling
├── genre_workshopping/           # Pre-wired packs in design
├── runs/                         # Local generation outputs (gitignored)
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

## Image assets (LFS)

Image assets that remain LFS-tracked are unaffected by the audio-in-R2 change.
Binary assets are tracked with Git LFS.

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
git remote set-url origin git@github.com:slabgorb/sidequest-content.git
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

- [orc-quest](https://github.com/slabgorb/orc-quest) — Orchestrator, ADRs
- [sidequest-server](https://github.com/slabgorb/sidequest-server) — Python FastAPI backend
- [sidequest-daemon](https://github.com/slabgorb/sidequest-daemon) — Python media services
- [sidequest-ui](https://github.com/slabgorb/sidequest-ui) — React client

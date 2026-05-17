# CLAUDE.md — SideQuest Content

Genre packs for SideQuest — YAML configs, audio, images, and world-building content.

## CRITICAL: Personal Project

This is a personal project under the `slabgorb` GitHub account.
- **No Jira integration.** Never create, reference, or interact with Jira tickets.
- **No 1898 org.** Nothing goes to the work GitHub org. Ever.
- All repos live under `github.com/slabgorb/`.

## SideQuest System Overview

Four repos compose the SideQuest stack (Python backend per ADR-082, ported from the Rust prototype 2026-04):
- **sidequest-server** — Python/FastAPI game engine and WebSocket API on port 8765
- **sidequest-ui** — React/TypeScript game client (Vite, port 5173)
- **sidequest-daemon** — Python media services (image gen, audio library playback)
- **sidequest-content** — Genre packs (YAML configs, audio, images, world data)

Orchestrator repo (`orc-quest`, also cloned as `oq-1` / `oq-2`) coordinates sprint tracking, docs, ADRs, and cross-repo scripts.

## Quality Rules

- No stubs, no hacks, no "we'll fix it later" shortcuts
- No skipping tests to save time
- No half-wired features — connect the full pipeline or don't start
- If something needs 5 connections, make 5 connections. Don't ship 3 and call it done.
- **Never say "the right fix is X" and then do Y.** Do X.
- **Never downgrade to a "quick fix" because you think the context is "just a playtest."**
  Every playtest is production tomorrow. Fix it right.

## Development Principles

### No Silent Fallbacks
If something isn't where it should be, fail loudly. Never silently try an alternative
path, config, or default. Silent fallbacks mask configuration problems and lead to
hours of debugging "why isn't this quite right."

### No Stubbing
Don't create stub implementations, placeholder modules, or skeleton code. If a feature
isn't being implemented now, don't leave empty shells for it. Dead code is worse than
no code.

### Don't Reinvent — Wire Up What Exists
Before building anything new, check if the infrastructure already exists in the codebase.
Many systems are fully implemented but not wired into the server or UI. The fix is
integration, not reimplementation.

### Verify Wiring, Not Just Existence
When checking that something works, verify it's actually connected end-to-end. Tests
passing and files existing means nothing if the component isn't imported, the hook isn't
called, or the endpoint isn't hit in production code. Check that new code has non-test
consumers.

### Every Test Suite Needs a Wiring Test
Unit tests prove a component works in isolation. That's not enough. Every set of tests
must include at least one integration test that verifies the component is wired into the
system — imported, called, and reachable from production code paths.

### Backend Language
The server (`sidequest-server`) is Python/FastAPI per ADR-082, ported from a
Rust prototype in 2026-04. The Rust codebase is preserved read-only at
https://github.com/slabgorb/sidequest-api for historical reference; older ADRs
that show Rust code are historical illustration only — see `docs/adr/README.md`
for the translation table. New backend code goes in Python. Media services
(`sidequest-daemon`) remain Python for inference library maturity (Z-Image / ACE-Step). The narrator LLM path uses the Anthropic Python SDK by default
per ADR-101 (supersedes ADR-001; `claude -p`/Ollama are opt-in non-default
backends). (Kokoro TTS was formerly in this list; TTS has been removed
from the system.)

## OTEL Observability Principle

Every backend fix that touches a subsystem MUST add OTEL watcher events so the GM panel
can verify the fix is working. Claude is excellent at "winging it" — writing convincing
narration with zero mechanical backing. The only way to catch this is OTEL logging on
every subsystem decision:

- **Intent classification** — what was the action classified as, and why?
- **Agent routing** — which agent handled the action?
- **State patches** — what changed in game state (HP, location, inventory)?
- **Inventory mutations** — items added/removed, with source
- **NPC registry** — NPCs detected, names assigned, collisions prevented
- **Trope engine** — tick results, keyword matches, activations
- **Encounter engine** — beat selections, metric changes, resolution

The GM panel is the lie detector. If a subsystem isn't emitting OTEL spans, you can't
tell whether it's engaged or whether Claude is just improvising.

**Not needed for:** Cosmetic UI changes (labels, spacing, colors).

## Architecture Decision Index

ADRs live in the orchestrator repo at `orc-quest/docs/adr/`. See
`orc-quest/docs/adr/README.md` for the canonical index. Before designing
or modifying a subsystem, check the relevant ADR:

Particularly relevant to this content repo:

| Domain | ADRs |
|--------|------|
| Genre packs | 003 (pack architecture), 004 (lazy binding) |
| Pack-side mechanics | 014 (diamonds/coal), 018 (trope engine), 020 (NPC disposition), 022 (world maturity), 033 (confrontation engine), 077 (dogfight), 078 (edge/composure), 093 (confrontation calibration), 095 (class mechanical surface) |
| Cultures / naming | 091 (culture-corpus Markov naming) |
| Music | 095 (daemon music tier via ACE-Step) — `*_input_params.json` lives here, OGG lives in R2 |
| Image style | 086 (image-composition taxonomy — portrait / POI / illustration), 070 (MLX / Z-Image renderer), `PROMPTING_Z_IMAGE.md` in this repo |
| Cartography | 019 (cartography config — runtime fog-of-war view retired 2026-04-28, see SUPERSEDED), 055 (room graph navigation), 089 (cavern template generation), 096 (cavern renderer revival) |
| Worlds | 053 (scenario system — clue graph, belief state, gossip) |

For the full ADR index see `orc-quest/docs/adr/README.md`.
Drift: `orc-quest/docs/adr/DRIFT.md`. Superseded: `orc-quest/docs/adr/SUPERSEDED.md`.

## Spoiler Protection

- **Fully spoilable:** `mutant_wasteland/flickering_reach` only
- **Fully unspoiled:** Everything else

## Asset Hosting

> **Both audio and image assets are NOT in this repo.** They live in R2
> (`cdn.slabgorb.com`). What lives in git is the *spec* (prompts, manifests,
> generation parameters) — the rendered binary lives in R2.
>
> - **Audio:** per-track ACE-Step generation parameters live at
>   `genre_packs/<pack>/audio/music/*_input_params.json` (ADR-095). The OGG
>   lives in R2. Regenerate with
>   `python scripts/generate_music.py --genre <pack>` from the orchestrator.
> - **Images:** `portrait_manifest.yaml`, POI yaml files, and Z-Image prompt
>   text in `visual_style.yaml` are the canonical spec. The rendered PNGs
>   live in R2 at the same relative path under `genre_packs/<pack>/…`.
>   Render scripts (`scripts/generate_portrait_images.py`,
>   `generate_poi_images.py`, `generate_creature_images.py`) write PNGs into
>   the local workspace; `.gitignore` keeps them out of commits.
>   `scripts/r2_sync_packs.py` uploads from the workspace to R2.

**Never commit fresh PNG/JPG/WebP assets through git-LFS.** The
`.gitattributes` file still has `*.png filter=lfs` rules as residue from the
pre-R2 era, but the `.gitignore` in `genre_packs/**/images/**` and friends
prevents accidental commits. A few historical LFS objects remain in the
test-fixture tree (`tools/cavern_renderer/tests/fixtures/`) — those stay.

## Syncing Between Machines

LFS-tracked binaries have a 10 GiB/month bandwidth budget on GitHub Pro.
With audio and images both in R2, the bandwidth concern is minor — but
`.safetensors` LoRA weights still ride LFS. **Do not pull from GitHub to
sync between local repos** when LoRA weights are part of the diff.

Instead, each clone has a `local` remote pointing to the other machine's copy:

```bash
# Sync from the other local repo (no GitHub bandwidth)
git pull local main

# Only push to origin when you want a remote backup
git push origin main
```

### First-time setup on a new machine

Clone from an existing local copy, then fix the remotes:

```bash
# Clone locally (not from GitHub)
git clone --no-hardlinks /path/to/existing/sidequest-content /path/to/new/sidequest-content

# Point origin at GitHub for backup pushes
cd /path/to/new/sidequest-content
git remote set-url origin git@github.com:slabgorb/sidequest-content.git

# Add the source as a local remote for future syncing
git remote add local /path/to/existing/sidequest-content
```

### Current local remotes

| Machine | Path | Local remote points to |
|---------|------|----------------------|
| OQ-1 | `/Users/slabgorb/Projects/oq-1/sidequest-content` | (primary copy) |
| OQ-2 | `/Users/slabgorb/Projects/oq-2/sidequest-content` | OQ-1 path above |

## Consumers

- **sidequest-server** (Python) — `SIDEQUEST_GENRE_PACKS` env var
- **sidequest-daemon** (Python) — `SIDEQUEST_GENRE_PACKS` env var
- **orchestrator justfile** — `content` variable points here
- **scripts/** in orchestrator — `generate_poi_images.py`, `generate_music.py`, etc.

## Structure

Live, wired packs (loaded by server + daemon at runtime):

```
genre_packs/
├── caverns_and_claudes/  # Classic dungeon crawl (meta-humor on D&D tropes)
├── elemental_harmony/    # Martial arts / elemental magic
├── mutant_wasteland/     # Post-apocalyptic mutants
├── space_opera/          # Sci-fi space adventure
└── tea_and_murder/       # Cosy Edwardian BritBox murder mystery (Glenross — Highland village amateur sleuths)
```

Workshopping packs (not yet wired into runtime) live under `genre_workshopping/` — heavy_metal, low_fantasy, neon_dystopia, pulp_noir, road_warrior, spaghetti_western at various levels of completeness.

Each pack contains YAML configs (archetypes, tropes, rules, encounters, factions, OCEAN profiles, conlang morphemes, audio cues, `visual_style.yaml`), world data, ACE-Step music params (`audio/music/*_input_params.json` — ADR-095, OGG lives in R2), and image prompts (portrait_manifest.yaml, POI yamls — rendered PNGs live in R2 at `cdn.slabgorb.com/genre_packs/<pack>/...`).

See `README.md` in this repo for the full taxonomy.

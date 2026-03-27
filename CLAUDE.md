# sidequest-content

Genre packs for SideQuest — YAML configs, audio, images, and world-building content.

## Syncing Between Machines

Binary assets are tracked with Git LFS. **Do not pull from GitHub to sync between local repos** — it eats LFS bandwidth (10 GiB/month limit on GitHub Pro).

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
| OQ-1 | `/Users/keithavery/Projects/sidequest-content` | (primary copy) |
| OQ-2 | `/Users/keithavery/Projects/oq-2/sidequest-content` | OQ-1 path above |

## Consumers

- **sidequest-api** (Rust) — `--genre-packs-path` CLI arg
- **sidequest-daemon** (Python) — `SIDEQUEST_GENRE_PACKS` env var, or auto-detected via `config.py`
- **orchestrator justfile** — `content` variable points here
- **scripts/** in orchestrator — `generate_poi_images.py`, `generate_music.py`, etc.

## Structure

```
genre_packs/
├── elemental_harmony/    # Martial arts / elemental magic
├── low_fantasy/          # Gritty medieval
├── mutant_wasteland/     # Post-apocalyptic mutants
├── neon_dystopia/        # Cyberpunk
├── pulp_noir/            # 1930s detective
├── road_warrior/         # Vehicular post-apocalypse
└── space_opera/          # Sci-fi space adventure
```

Each pack contains YAML configs (archetypes, tropes, rules, etc.), world data, audio tracks, and images (portraits, POI landscapes).

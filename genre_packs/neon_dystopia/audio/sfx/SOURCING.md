# SFX Sourcing — Neon Dystopia

All effects are sourced and present on disk. This file is the inventory,
not a TODO list. Licensing is mixed — some effects derive from the commercial
**Game SFX Ultimate Bundle** (see `sound_effects/README.md` at the content
repo root), others from CC0 libraries (Kenney, Freesound). Per-file attribution
below is best-effort and should be reconciled against the purchase receipt
before any public release.

## Present Effects

| File | Description |
|------|-------------|
| `chrome_deploy.ogg` | Cybernetic chrome implant activation |
| `comm_ring.ogg` | Communication device notification |
| `crowd_murmur.ogg` | Oppressed crowd background |
| `cyberblade.ogg` | Energy blade activation / swing |
| `door_hydraulic.ogg` | Hydraulic / pneumatic door |
| `gunshot.ogg` | Sci-fi weapon discharge |
| `hack_breach.ogg` | Netrunner breach sting |
| `neon_hum.ogg` | Electric hum of neon signage |
| `rain.ogg` | Acid rain ambience |
| `vehicle_engine.ogg` | Hover / ground vehicle pass-by |

## Sources

- **Game SFX Ultimate Bundle** — Daniel Nunez Martin, commercial (https://en.danielnunezmartin.com/). See `sound_effects/README.md`.
- **Kenney.nl** — CC0 game assets: https://kenney.nl/assets?q=audio
- **Freesound** — CC0 filtered search: https://freesound.org

Mixed licensing. Any new SFX must be either CC0 or sourced from a licensed
commercial bundle whose terms permit game distribution. No
attribution-required-only licenses (CC-BY) without recording the attribution
in this file.

## Format

- OGG Vorbis, quality 4
- Mono or stereo, 44.1kHz
- Normalized to -16 LUFS (matches music track loudness)
- Filename matches `sfx_library` key in `pack.yaml`

# Low Fantasy Audio Asset Pack — Credits & Sources

Music in this pack is generated with [ACE-Step](https://github.com/stepfun-ai/ACE-Step)
at build time from prompt parameter files (`*_input_params.json`) that live
alongside each `.ogg`. The full set of moods — combat, exploration, mystery,
rest, sorrow, tavern, tension — is present with ambient / sparse / full /
overture / resolution / tension_build variants driven by the scene interpreter.

SFX are sourced from CC0 / public-domain libraries (primarily Kenney and
Freesound) and mixed through `audio/mixer.py` in the daemon.

## Music

- **Source:** ACE-Step local generation (see `scripts/generate_music.py` in the orchestrator).
- **License:** Model output — no attribution required. The `_input_params.json`
  files are the canonical record of how each track was produced; keep them
  alongside any regenerated variant.

## SFX

- **Kenney** (kenney.nl) — CC0 game-audio packs (RPG Audio, Impact Sounds, Interface)
- **Freesound** (freesound.org) — CC0 community uploads only (filter by license)
- **Pixabay** (pixabay.com) — Royalty-free under the Pixabay License

No attribution-required assets are permitted in this pack. If you add a new
effect that requires attribution, credit the artist in this file and verify
the license on the source page.

## Format

- Music: OGG Vorbis, stereo, 44.1kHz, ACE-Step defaults
- SFX: OGG Vorbis quality 4, mono or stereo, 44.1kHz
- Filenames match the mood / sfx_library key used in `pack.yaml`

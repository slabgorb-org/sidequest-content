# Purchased Audio — Provenance & Routing

Externally-sourced music tracks added to genre-pack `audio.yaml` manifests.
Unlike ACE-Step tracks (which carry a reproducible `*_input_params.json` spec),
these are commercial purchases with no generation spec — **this file is the only
re-upload record.** The OGG lives in R2 only (per repo convention); the YAML
references it; the source masters live in the buyer's local library.

## Source: TableTop Audio "Ambient Environments" (DriveThruRPG)

Local masters: `~/Documents/DriveThruRPG/Ambient Environments/`
Encode recipe: `ffmpeg -i <src> -map 0:a:0 -c:a libopus -b:a 96k <out>.ogg`
(matches the daemon music pipeline — Opus-in-OGG, 96k). FLAC source preferred
where available, else 320k MP3. All tracks ~600s ambient loops.

License note: these are commercial TableTop Audio tracks. Serving them via
`cdn.slabgorb.com` is acceptable for private, Zero-Trust-gated playgroup use;
public redistribution of the standalone files is a licensing concern.

## Wired

| Source track | OGG path | Pack | Mood |
|--------------|----------|------|------|
| The Streets of Seattle 2072 | neon_dystopia/audio/music/streets_of_seattle_2072.ogg | neon_dystopia | exploration |
| The Streets of Seattle 2072 | space_opera/audio/music/streets_of_seattle_2072.ogg | space_opera | exploration |
| Black ICE | neon_dystopia/audio/music/black_ice.ogg | neon_dystopia | cyberspace |
| Black ICE | space_opera/audio/music/black_ice.ogg | space_opera | combat |
| Hacking In | neon_dystopia/audio/music/hacking_in.ogg | neon_dystopia | cyberspace |
| Syndicate | neon_dystopia/audio/music/syndicate.ogg | neon_dystopia | corporate |
| Syndicate | space_opera/audio/music/syndicate.ogg | space_opera | drift |
| Sabotage | neon_dystopia/audio/music/sabotage.ogg | neon_dystopia | tension |
| Sabotage | space_opera/audio/music/sabotage.ogg | space_opera | combat |
| Dungeon Crawling | caverns_and_claudes/audio/music/dungeon_crawling.ogg | caverns_and_claudes | exploration |
| Lost in the Labyrinth | caverns_and_claudes/audio/music/lost_in_the_labyrinth.ogg | caverns_and_claudes | exploration |
| Egyptian Tomb | caverns_and_claudes/audio/music/egyptian_tomb.ogg | caverns_and_claudes | exploration |
| Tomb of the Ancients | caverns_and_claudes/audio/music/tomb_of_the_ancients.ogg | caverns_and_claudes | exploration |
| Catacombs | caverns_and_claudes/audio/music/catacombs.ogg | caverns_and_claudes | tension |
| Temple of Dread | caverns_and_claudes/audio/music/temple_of_dread.ogg | caverns_and_claudes | tension |
| Defiling the Crypt | caverns_and_claudes/audio/music/defiling_the_crypt.ogg | caverns_and_claudes | combat |
| Radioactive Wasteland | mutant_wasteland/audio/music/radioactive_wasteland.ogg | mutant_wasteland | exploration |
| Battlefield Ruins | mutant_wasteland/audio/music/battlefield_ruins.ogg | mutant_wasteland | ruins |
| Battlefield Ruins | road_warrior/audio/music/battlefield_ruins.ogg | road_warrior | exploration |
| Old Western Town | spaghetti_western/audio/music/old_western_town.ogg | spaghetti_western | exploration |
| Old Western Saloon | spaghetti_western/audio/music/old_western_saloon.ogg | spaghetti_western | saloon |
| Wild West Showdown | spaghetti_western/audio/music/wild_west_showdown.ogg | spaghetti_western | standoff |
| Reckoning | spaghetti_western/audio/music/reckoning.ogg | spaghetti_western | standoff |

### KS3 Music Sound Pack — wired (heavy_metal only; FLAC source)

Keith's call (2026-05-25): wire only what fits heavy_metal's funereal-baroque
tone; hold the rest. Source: `KS3-Music Sound Pack/Music_Sound_Pack_FLAC-{A,B,C}/`.

| Source track | OGG path | Pack | Mood |
|--------------|----------|------|------|
| A Dwarven Farewell | heavy_metal/audio/music/dwarven_farewell.ogg | heavy_metal | sorrow |
| The Desolate Expanse | heavy_metal/audio/music/the_desolate_expanse.ogg | heavy_metal | tension |
| Battle Hymn of War | heavy_metal/audio/music/battle_hymn_of_war.ogg | heavy_metal | combat |
| The Monolith | heavy_metal/audio/music/the_monolith.ogg | heavy_metal | ritual |
| Angelic Voices | heavy_metal/audio/music/angelic_voices.ogg | heavy_metal | ritual |

### SciFi Atmosphere Loops Vol1 — wired (space_opera; WAV source)

Keith's call (2026-06-07): wire all 8. Source:
`~/Downloads/SciFi_Atmosphere_Loops_Vol1/*.wav` (~60s atmosphere loops,
~90s reactor loops). Encode recipe as above (libopus 96k).

**Special case — "3 Dark" OVERWRITES an ACE-Step key:** the set-1 exploration
*ambient* leitmotif variation (`audio/music/set-1/exploration_ambient.ogg`)
was nuked by operator decision ("that one was terrible") and its R2 object
replaced in place so the themes-block variation machinery needs no change.
No `*_input_params.json` ever existed for that key (pre-ADR-095 batch) —
nothing will regenerate over it, but if a set-1 params backfill ever happens,
SKIP this key.

| Source track | OGG path | Pack | Mood |
|--------------|----------|------|------|
| 3 Dark | space_opera/audio/music/set-1/exploration_ambient.ogg | space_opera | exploration theme · ambient variation (in-place replacement) |
| 1 Full | space_opera/audio/music/scifi_atmosphere_full.ogg | space_opera | exploration |
| 2 Texture | space_opera/audio/music/scifi_atmosphere_texture.ogg | space_opera | drift |
| 4 Pulse And Texture | space_opera/audio/music/scifi_atmosphere_pulse_texture.ogg | space_opera | tension |
| 5 Reactor Full | space_opera/audio/music/scifi_reactor_full.ogg | space_opera | docking |
| 6 Reactor Dark | space_opera/audio/music/scifi_reactor_dark.ogg | space_opera | void |
| 7 Reactor Movement | space_opera/audio/music/scifi_reactor_movement.ogg | space_opera | drift |
| 8 Reactor Intense | space_opera/audio/music/scifi_reactor_intense.ogg | space_opera | tension |

## Held — not wired (no clear home)

- **Nyarlathotep**, **The Dreams in the Witch House**, **The Lurker at the
  Threshold** — Cthulhu Mythos cosmic horror. No cosmic-horror pack exists.
  Candidate: caverns_and_claudes/beneath_sunden keeper/tension (the Glutton
  entity), or a future horror pack. Decision: hold (2026-05-25).
- **KS3 Music Sound Pack — remaining 19 tracks.** Too light/bardic/pastoral for
  heavy_metal; no other tonally-correct *wired* home (caverns is silence=danger).
  Decision: hold (2026-05-25).
  - **Pirate (4)** — Jolly Pirate Song, Pieces of Eight, Pirate Accordian Song,
    Pirate Song Two. Held as a seed for a future pirate/high-seas pack.
  - **Bardic/tavern (8)** — Tavern Song, The Minstrel's Song 1 & 2, Song of the
    Troubador, Bard on the Fife and Drum, Bard on the Zither, Female Bard Song,
    Female Bard and Minstrel's. Held; no wired home — seed for a future tavern/folk pack.
  - **Pastoral/medieval (5)** — Return to the Capital City, The Quaint Village,
    Elven Sanctuary, Hovel in the Sunlight, Action Sequence. Held; no wired home.
  - **Off-genre (2)** — Planet X, Arabian Desert Music. Easy follow-ups if wanted:
    Planet X → space_opera (drift/void); Arabian Desert → elemental_harmony
    (exploration, eastern). Not wired pending Keith's go.

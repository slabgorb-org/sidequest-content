# Shared PD Jazz Recordings — Bucket & Backlog

This bucket holds **genuine public-domain jazz recordings** (real 1920s 78rpm
transfers), as distinct from `../ragtime_pd/` (composer-*rendered* Joplin scores)
and `../classical_pd/` (composer-rendered classical scores). A track here is an
actual recording, transcoded to OGG and uploaded to R2 — NOT synthesized.

Audio path convention is identical: a pack `audio.yaml` references
`assets/audio/jazz_pd/<file>.ogg`, which resolves to the shared bucket (no pack
slug). The `.ogg` is gitignored and lives on R2; this file is the tracked spec.

## Pipeline (no composer — recordings, not notation)
1. Source the 78rpm transfer from the Internet Archive item `1920sJazz_201606`
   (`https://archive.org/download/1920sJazz_201606/<file>.mp3`).
2. Transcode + loudness-normalize to match the rendered buckets:
   `ffmpeg -i "<in>.mp3" -af "loudnorm=I=-16:TP=-1.5:LRA=11" -ar 44100 -c:a libvorbis -q:a 5 "<out>.ogg"`
   (use the composer's bundled static ffmpeg — Homebrew ffmpeg lacks libvorbis).
3. Upload via `scripts/r2_sync_packs.sync(content_root, files=[...])`, then
   `scripts/r2_manifest_from_bucket.py`.

## CRITICAL — US public-domain rule (Music Modernization Act / CPAA)
A US sound recording is PD iff **first published in 1925 or earlier** (as of 2026).
Recordings published 1923–1946 get a 100-year term, entering PD on **Jan 1 of
(publication year + 101)**: 1925→2026, 1926→2027, 1927→2028, 1928→2029, 1929→2030…
**The recording date is what's copyrighted, not the song's composition date** —
several titles below are old songs but *late* cuts. An archive.org "Public Domain
Mark" is user-applied and NOT authoritative; verify the actual recording year.
(The original `jazz_pd/LICENSE.md`, now removed, wrongly claimed all 1923–1928
sides were PD as of 2024. They are not.)

## Status — 18 tracks from `1920sJazz_201606`

### ✅ Wired (PD now)
| Track | Artist / recording | Year | PD since | Status |
|---|---|---|---|---|
| Helen Gone | Vincent Rose & His Montmartre Orch. — Victor 19378 | 1924 | 2025-01-01 | **LIVE** (pulp_noir tavern/speakeasy) |
| Montmartre Rag | Mitchell's Jazz Kings (Paris, Pathé) | 1922 | 2023-01-01 | **LIVE** (pulp_noir tavern/speakeasy, chase) |
| Dipper Mouth Blues | King Oliver's Creole Jazz Band | 1923 | 2024-01-01 | **LIVE** (pulp_noir combat, tavern/speakeasy) |
| Tiger Rag | Original Dixieland Jazz Band — Victor 18472-B | 1918 | 2022-01-01 | **LIVE** (pulp_noir combat, chase) |
| Crazy Blues | Mamie Smith & Her Jazz Hounds — OKeh | 1920 | 2022-01-01 | **LIVE** (pulp_noir tension, intrigue) |
| Weeping Willow Blues | Bessie Smith — Columbia (rec. 1924-09-26) | 1924 | 2025-01-01 | **LIVE** (pulp_noir tension, intrigue) |
| St. Louis Blues | Bessie Smith w/ Louis Armstrong — Columbia (rec. 1925-01-14) | 1925 | 2026-01-01 | **LIVE** (pulp_noir rest, intrigue) |

> **2026-06-14 sourcing pass — the 1917–1925 hot-jazz seam.** The original
> `1920sJazz_201606` set was mostly 1926+ (deferred below). This pass instead
> mined the *earlier* window that is already PD, as individual Internet Archive
> items (not the `1920sJazz_201606` compilation):
>   - Montmartre Rag — `1922-B-Archives-1922-07-00-Mitchells-Jazz-Kings-Montmartre-rag-Paris`
>   - Dipper Mouth Blues — `1923-USA-Archives-1923-00-00-King-Olivers-Creole-Jazz-Band-Dipper-Mouth-Blues`
>   - Tiger Rag — `original-dixieland-jazz-band-tiger-rag-victor-18472-b`
>   - Crazy Blues — `MamieSmithHerJazzHounds`
>   - Weeping Willow Blues — `bessie-smith-weeping-willow-blues` (date 1924-09-26)
>   - St. Louis Blues — `the-st-louis-blues` (date 1925-01-14)
> Transcoded with the composer's static libvorbis ffmpeg per the pipeline below.
> Also removed pulp_noir's `themes:` block in the same change — it was shadowing
> mood_tracks so NONE of this jazz (nor the Joplin ragtime) actually played.
>
> **REJECTED — Canal Street Blues** (`78_canal-street-blues_..._gbia0253734b`):
> recording is 1923 but THIS transfer is tagged `year: 1946` (reissue pressing).
> Per the verify-the-recording-year rule we did not wire it; King Oliver is
> already covered by the clean 1923 Dipper Mouth item. Re-source from a
> 1923-tagged Gennett transfer to clear it.

### ⏳ Backlog — enters PD on the dated schedule (wire each on/after its year)
| Enters PD | Track | Artist / recording | Rec. year |
|---|---|---|---|
| **2027-01-01** | Bell Hoppin' Blues | Ben Bernie & His Hotel Roosevelt Orch. — Brunswick 3082 | 1926 |
| **2027-01-01** | Here Comes Emaline | Joe Candullo & His Everglades Orch. — Harmony 208-H | 1926 |
| **2027-01-01** | Messin' Around | Cookie's Gingersnaps (Freddie Keppard) — OKeh 8390 | 1926 |
| **2027-01-01** | Stampede | (Fletcher Henderson) — Victor 20460-A | 1926 |
| **2028-01-01** | Baby Your Mother | Don Bestor & His Orch. — Victor | 1927 |
| **2028-01-01** | Cuddle Closer | Cole McElroy's Spanish Ballroom Orch. — Columbia 959-D | 1927 |
| **2028-01-01** | Gravier Street Blues | Clarence Williams' Jazz Kings — Columbia | 1927 |
| **2028-01-01** | Krazy Kat | Frankie Trumbauer & His Orch. (w/ Bix) — OKeh 40903 | 1927 |
| **2029-01-01** | Red Hot Pepper | (Jelly Roll Morton) — Victor V-38055-A | 1928 |
| **2030-01-01** | Bashful Baby | Ben Pollack & His Park Central Orch. — Victor | 1929 |
| **2030-01-01** | Blue Nights | Earl Hines & His Orch. — Victor V-38096 | 1929 |
| **2030-01-01** | Damp Weather Blues | Jones & Collins Astoria Hot Eight — OKeh | 1929 |
| **2031-01-01** | Keepin' Myself For You | The High Hatters (Belle Mann vcl) — Victor | 1930 |
| **2038-01-01** | Cryin' Mood | Clarence Williams & His Washboard Band — Bluebird | 1937 |
| **2039-01-01** | There'll Be Some Changes Made | Pee Wee Russell's Rhythmakers — HRS 1001 | 1938 |

### ❓ Unclear — needs a confirmed recording date before use
| Track | Artist / recording | Note |
|---|---|---|
| Last Night On The Back Porch | Royal Havana Orchestra | Song is 1923; pseudonym used only 1922–24, so the cut is *probably* 1923–24 (PD) — but the specific Banner-family disc catalog#/date is unconfirmed. Pin the catalog number to clear it. |
| Riverboat Shuffle | Bill Priestley / Squirrel Ashcraft | Private amateur "Sessions at Squirrel's" (Evanston), NOT the 1924 Wolverines. Post-1925, undatable precisely → treat as not clear. |

> To wire a backlog track once it clears: download from `1920sJazz_201606`,
> transcode per the pipeline above, add an `assets/audio/jazz_pd/<file>.ogg`
> entry to `pulp_noir/audio.yaml` (speakeasy/tavern/chase by tempo), upload, and
> move its row to "Wired" here.

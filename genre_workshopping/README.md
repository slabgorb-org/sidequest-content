# genre_workshopping/ — staging

This is the **staging** area for genre packs in development. Nothing here
is loaded by `sidequest-server` or `sidequest-daemon` at runtime — the
production packs live in `../genre_packs/`.

`SIDEQUEST_GENRE_PACKS` should not point here. If a player can pick a pack
from this directory in the UI, something is misconfigured.

## Why two directories

The server has no concept of a "draft" pack. Every directory under the path
named by `SIDEQUEST_GENRE_PACKS` is enumerated and offered as a selectable
genre. That means a half-built pack with missing archetypes or no portraits
would show up alongside finished content if it lived there. Splitting the
tree gives us a place to iterate without that risk.

A pack here can be:

- **Active workshop** — being authored, has substantive YAML / images /
  audio but does not yet meet the promotion gate.
- **Stub / leftover** — a small directory left behind after the pack was
  promoted into `../genre_packs/`. These can be cleaned up but are
  harmless; they are not loaded.

## Promotion to production

See `../genre_packs/README.md` for the promotion gate. A pack moves out of
this directory and into `../genre_packs/` once it has the full YAML set,
generated portraits and POI landscapes, indexed audio, and a successful
end-to-end playtest run.

When promoting, move the directory rather than copying it, and delete any
empty residue here. Two divergent copies of the same pack name across
production and staging is a footgun.

## Current packs

| Pack | Status |
|------|--------|
| `low_fantasy` | Active workshop — gritty medieval; substantive YAML, audio, images |
| `road_warrior` | Active workshop — vehicular post-apocalypse |
| `neon_dystopia` | Promoted 2026-05-23 to `../genre_packs/neon_dystopia/` (asset gate not yet met); workshop directory removed |
| `pulp_noir` | Promoted 2026-05-23 to `../genre_packs/pulp_noir/` (asset gate not yet met); workshop directory removed |
| `heavy_metal` | Re-promoted 2026-05-23 to `../genre_packs/heavy_metal/` (loads clean — 2 worlds, world openings + new-schema confrontations present; asset gate not yet met); workshop directory removed |
| `spaghetti_western` | Stub leftover — promoted into `../genre_packs/spaghetti_western/`; directory effectively empty |

## Editing rules

- Match the shape of an existing production pack (`../genre_packs/caverns_and_claudes/`
  is the canonical reference). Don't invent new top-level layouts here —
  reshaping after promotion is painful.
- Binary assets are still tracked with Git LFS even in workshop; commit
  generated images / audio normally.
- It is fine to commit a workshop pack with rough edges. It is not fine to
  point `SIDEQUEST_GENRE_PACKS` at this directory to "test" one.

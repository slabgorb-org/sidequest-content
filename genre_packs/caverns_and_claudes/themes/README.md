# Beneath Sünden — Theme Palette (scaffold)

Curated themed zone definitions for the `beneath_sunden` world. Loaded by
`sidequest.dungeon.themes.load_theme_palette` (server-native, spec §6/§8).
Schema authority: `sidequest-server/sidequest/dungeon/themes.py` +
`setpieces.py`.

**This is the Plan-4 scaffold** — one theme per interior generator class
(`cellular`/`depthfirst`/`prim`/`roomcorridor`) plus the deliberately
pristine `labyrinth_trap` (braid_ratio 0.0, spec §5.2). The *exhaustive*
curated palette + curation passes are **Plan 8** (spec §10 step 8).

- `depth_band` values are RAW `depth_score` units (Plan 3:
  `depth_per_hop = 10.0`), never player-facing "level" buckets.
- Every set-piece carries non-blank `telegraph` + `outcome` (spec §4 —
  the dungeon plays fair).
- `braid_ratio`: labyrinth-trap `0.0`; other maze themes `0.3`;
  `cellular`/`roomcorridor` `0.0` (braid is inert for non-perfect-maze
  generators).

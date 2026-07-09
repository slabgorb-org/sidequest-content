# Raster Map Anchor Calibrator

A standalone, offline browser tool for authoring and calibrating per-world
raster `map.yaml` `node_anchors` — the visual way to do the "calibrate anchors
against the real scan" step in every world's `assets/maps/README.md`.

Part of the Track A mapping work (spec `docs/superpowers/specs/2026-07-08-three-tier-mapping-design.md` §2,
plan `docs/superpowers/plans/2026-07-08-mapping-track-a-main-map-treatments.md`,
epic 163). It has **no runtime surface** — it's a dev/authoring aid only. Pairs
with the RasterMap UI (163-5).

## Files

| File | Role |
|------|------|
| `map-anchor-calibrator.html` | The generated, self-contained tool. Open in any browser. |
| `build_map_calibrator.py` | Generator — scans content and rebuilds the HTML. |
| `map-calibrator.template.html` | HTML/JS template the generator fills. |

## Use it

Open `tools/map-anchor-calibrator.html` in a browser (double-click, or
`open tools/map-anchor-calibrator.html`). No server, no network.

1. **Pick a world** from the grouped dropdown. Every world with a
   `cartography.yaml` is loaded. Worlds with a raster `map.yaml` seed from their
   real anchors (badge: `raster map.yaml`); the rest start from an auto-laid-out
   adjacency graph (badge: `no map yet`) so you can bootstrap a new map.
2. **Load the scan** (Background scan → file picker). Set opacity; toggle
   contain/stretch. **Match scan size** resets the working canvas to the image's
   real pixels and rescales the anchors.
3. **Place the pins.** Drag a pin, or click to select and type exact x/y or
   arrow-key nudge (⇧ = ×10). **Snap** to a grid, **align guides** snap to
   another pin's x/y, and a live **distance readout** shows px from the selected
   pin to the cursor.
4. **Edit the graph (optional).** *Edit adjacency* → click two pins to toggle a
   link. Rename a region in the selected-pin box. These export as a
   **cartography reference patch** you apply to `cartography.yaml` by hand — the
   tool never rewrites it.
5. **Export.** The `map.yaml` tab shows a live, paste-ready file (provenance +
   style_hints preserved, plus a working-canvas comment). Copy or download, then
   paste into the world's `map.yaml`.

## Important: anchors are scan-specific

`node_anchors` are **pixels within the working canvas**, calibrated against the
**one specific scan** you loaded. A different scan (different publisher, crop, or
resolution) shifts every pixel — re-calibrate if you swap the image. This is why
`image` + `provenance` must name the exact scan the anchors were dragged on.

Fill `provenance` from the real sourced scan (source / date / archive / pd_basis)
— a public-domain basis you can defend. Good examples already in-tree:
`spaghetti_western/the_real_mccoy` (Woods 1867 Pittsburgh, NYPL) and
`road_warrior/the_circuit`.

## Regenerate

Whenever content changes (a new world, a new/edited `map.yaml`, renamed
regions), rebuild the tool so its seeds are current:

```
python tools/build_map_calibrator.py            # stamps today's date
python tools/build_map_calibrator.py --date 2026-07-09   # pin the date for a reproducible diff
```

The generator is deterministic: same content in → identical HTML out (auto-layout
uses a fixed circular seed + fixed iteration count; only the build date varies).
Worlds without a raster `map.yaml` get a spring-layout of their adjacency graph
and a TODO provenance skeleton to fill.

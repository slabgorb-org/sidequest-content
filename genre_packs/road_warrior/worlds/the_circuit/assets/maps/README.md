# The Circuit main-map raster — authoring checklist

1. Source the PD scan: a mid-century US state highway department official road
   map (or a pre-war auto-trail atlas plate). These are US government works —
   public domain. A period highway map suits the road_warrior defacement style.
2. Save it here as `state_highway_map.jpg` (the `image:` in ../../map.yaml).
3. Calibrate `node_anchors` in ../../map.yaml against the real scan: open the
   image, read the [x, y] pixel of each region's landmark, replace the
   placeholders. Every one of the 13 regions MUST have an anchor (validator).
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate road_warrior` passes and the Map tab shows
   the scan with pins in place. The road_warrior theme renders routes as highway
   tracing and the faction layer as wasteland defacement (style_hints).

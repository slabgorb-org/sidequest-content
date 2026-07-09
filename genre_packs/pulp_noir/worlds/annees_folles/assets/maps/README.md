# Années Folles main-map raster — authoring checklist

1. Source the PD scan: an out-of-copyright Baedeker's Paris city plan from the
   David Rumsey Map Collection or BnF Gallica. Confirm publication pre-1929
   (copyright expired; public domain).
2. Save it here as `baedeker_paris_plan.jpg` (the `image:` in ../../map.yaml).
3. Calibrate `node_anchors` in ../../map.yaml against the real scan: open the
   image, read the [x, y] pixel of each arrondissement/quarter landmark, replace
   the placeholders. Every one of the 11 regions MUST have an anchor (validator).
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate pulp_noir` passes and the Map tab shows
   the scan with pins in place.

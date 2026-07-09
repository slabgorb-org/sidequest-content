# Années Folles main-map raster — authoring checklist

1. Source the PD scan: **Ward, Lock & Co.'s Plan of the City of Paris** (from a
   Ward Lock Guide to Paris, early 20th century). Published pre-1929 — public
   domain in the US. (A Baedeker Paris plan from David Rumsey / BnF Gallica is an
   equally valid alternative, but the anchors below were calibrated on the Ward
   Lock plan — swapping to a different scan means re-calibrating.)
2. Save it here as `ward_lock_paris_plan.jpg` (the `image:` in ../../map.yaml).
3. `node_anchors` in ../../map.yaml are calibrated against the Ward Lock plan on
   a 1024×768 canvas (via the map-anchor-calibrator tool). Re-place them if you
   swap the scan. Every one of the 11 regions MUST have an anchor (validator).
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate pulp_noir` passes and the Map tab shows
   the scan with pins in place.

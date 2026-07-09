# Glenross main-map raster — authoring checklist

1. Source the PD scan: an out-of-copyright Ordnance Survey One-Inch sheet
   covering the Glenross area from the National Library of Scotland
   (maps.nls.uk). Confirm publication >50 years ago (Crown copyright expired).
2. Save it here as `os_one_inch_glenross.jpg` (the `image:` in ../../map.yaml).
3. Calibrate `node_anchors` in ../../map.yaml against the real scan: open the
   image, read the [x, y] pixel of each region's landmark, replace the
   placeholders. Every one of the 14 regions MUST have an anchor (validator).
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate tea_and_murder` passes and the Map tab shows
   the scan with pins in place.

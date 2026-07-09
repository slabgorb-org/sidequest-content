# Glenross main-map raster — authoring checklist

1. Source the PD scan: an out-of-copyright large-scale Ordnance Survey sheet
   covering the Glenross-analogue parish (the real Aldunie / Ballhillock /
   Kirktown area along the Rouster Water) from the National Library of Scotland
   (https://maps.nls.uk/townplans/). Crown copyright expired (published >50
   years ago); NLS provides it freely. Confirm the exact sheet date.
2. Save it here as `os_glenross_nls.jpg` (the `image:` in ../../map.yaml).
3. Calibrate `node_anchors` in ../../map.yaml against the real scan with the
   map-anchor-calibrator tool (tools/map-anchor-calibrator.html): drag each of
   the 14 region pins onto its chosen feature — e.g. the_manse → the "Manse",
   the_post_office → "Post Office", the_school → "School", the_kirk_of_st_maelrubha
   → "Church", the_distillery → the mill by the burn. Every one of the 14 regions
   MUST have an anchor (validator).
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate tea_and_murder` passes and the Map tab shows
   the scan with pins in place.

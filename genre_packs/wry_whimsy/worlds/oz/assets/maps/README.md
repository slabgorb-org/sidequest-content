# Oz main-map raster — authoring checklist

1. Source the PD scan: Baum's **"Map of the Marvelous Land of Oz"** (drawn by
   "Prof. Wogglebug T.E."), the double-page endpaper map from *Tik-Tok of Oz*
   (1914). Published 1914 — public domain in the US (pre-1929). Widely available
   on Wikimedia Commons.
2. Save it here as `baum_oz_1914.jpg` (the `image:` in ../../map.yaml).
3. `node_anchors` in ../../map.yaml were calibrated against this exact scan on a
   1200×840 working canvas. A different scan (different crop/resolution) shifts
   every pixel — re-open the calibrator and re-place the pins if you swap it.
   Every one of the 7 regions MUST have an anchor (validator).
   Note Baum's map quirk: the compass is drawn with **East on the left**, so
   Munchkin Country (canonically East) sits on the left/blue quadrant.
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate wry_whimsy` passes and the Map tab shows the
   scan with pins in place.

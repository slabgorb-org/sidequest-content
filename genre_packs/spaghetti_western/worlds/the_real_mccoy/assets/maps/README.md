# The Real McCoy main-map raster — authoring checklist

1. Source the PD scan: **Woods' New Map of Pittsburgh, Allegheny and Surroundings**
   (1867, A. Hani lithographer), from the New York Public Library digital
   collections (also mirrored at old-maps.com). An 1867 US lithograph is public
   domain (published well before 1929). The world is set in 1878 — this
   period-close plan predates the setting by ~11 years, which is fine.
2. Save it here as `woods_pittsburgh_1867.jpg` (the `image:` in ../../map.yaml).
3. `node_anchors` in ../../map.yaml were calibrated against this exact scan on a
   1024×768 working canvas. If you substitute a different scan (different crop or
   resolution), re-open the calibrator and re-place the pins — pixel anchors are
   specific to the scan they were dragged on. Every one of the 11 regions MUST
   have an anchor (validator).
4. Upload to R2 (canonical media source) via the orchestrator scripts:
   `python scripts/r2_sync_packs.py` then `python scripts/r2_manifest_from_bucket.py`
   (run from the orchestrator root; these are separate manual steps — render/copy
   scripts do NOT auto-upload).
5. Verify: `just content-validate spaghetti_western` passes and the Map tab shows
   the scan with pins in place.

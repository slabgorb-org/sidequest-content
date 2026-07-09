#!/usr/bin/env python3
"""Generate the standalone raster-map anchor calibrator (map-anchor-calibrator.html).

Scans every ``genre_packs/*/worlds/*/cartography.yaml``, pulls each world's
regions (id, display name, adjacency), and seeds the calibrator:

* Worlds that already ship a raster ``map.yaml`` are seeded from its real
  ``node_anchors`` / ``provenance`` / ``style_hints`` (and its header comment
  is preserved verbatim).
* Worlds with no raster map yet get a deterministic spring-layout of their
  adjacency graph as a starting placeholder, plus a TODO provenance skeleton,
  so the tool can bootstrap a brand-new ``map.yaml``.

The data is injected into ``map-calibrator.template.html`` (the ``__DATA__`` and
``__GENMETA__`` placeholders) and written to ``map-anchor-calibrator.html``.

Run from the content repo root:  python tools/build_map_calibrator.py
Deterministic: same content in → identical HTML out (layout uses a fixed
circular seed + fixed iteration count; the only volatile field is the build
date, which you can pin with --date).
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import math
import os
import re
import sys

import yaml

CANVAS_W, CANVAS_H = 1024, 768
MARGIN = 0.08  # unit-space margin for auto-layout

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
TEMPLATE = os.path.join(HERE, "map-calibrator.template.html")
OUT = os.path.join(HERE, "map-anchor-calibrator.html")


def _load_yaml(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or {}
    except Exception as exc:  # fail loud per repo doctrine, but keep the build going per-world
        print(f"  ! could not parse {path}: {exc}", file=sys.stderr)
        return {}


def _leading_comment(path: str) -> list[str]:
    """Return the leading ``#`` comment lines of a YAML file (verbatim)."""
    out: list[str] = []
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                s = line.rstrip("\n")
                if s.startswith("#"):
                    out.append(s)
                elif s.strip() == "":
                    if out:
                        break
                else:
                    break
    except OSError:
        pass
    return out


def _pack_ruleset(pack_dir: str) -> str:
    rp = os.path.join(pack_dir, "rules.yaml")
    if os.path.exists(rp):
        return str(_load_yaml(rp).get("ruleset", "") or "")
    return ""


def spring_layout(ids: list[str], edges: set[tuple[str, str]]) -> dict[str, tuple[int, int]]:
    """Deterministic Fruchterman-Reingold layout in the 1024x768 frame.

    Nodes start on a circle (no RNG → reproducible), then relax under
    edge attraction + all-pairs repulsion. Single node → centre.
    """
    n = len(ids)
    if n == 0:
        return {}
    if n == 1:
        return {ids[0]: (CANVAS_W // 2, CANVAS_H // 2)}
    idx = {rid: i for i, rid in enumerate(ids)}
    pos = {}
    for i, rid in enumerate(ids):
        ang = 2 * math.pi * i / n
        pos[rid] = [0.5 + 0.34 * math.cos(ang), 0.5 + 0.34 * math.sin(ang)]
    k = 0.9 * math.sqrt(1.0 / n)
    adj = [(a, b) for (a, b) in edges if a in idx and b in idx]
    temp = 0.10
    iters = 320
    for _ in range(iters):
        disp = {rid: [0.0, 0.0] for rid in ids}
        for i in range(n):
            for j in range(i + 1, n):
                a, b = ids[i], ids[j]
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 1e-4
                f = (k * k) / d
                ux, uy = dx / d, dy / d
                disp[a][0] += ux * f
                disp[a][1] += uy * f
                disp[b][0] -= ux * f
                disp[b][1] -= uy * f
        for a, b in adj:
            dx = pos[a][0] - pos[b][0]
            dy = pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 1e-4
            f = (d * d) / k
            ux, uy = dx / d, dy / d
            disp[a][0] -= ux * f
            disp[a][1] -= uy * f
            disp[b][0] += ux * f
            disp[b][1] += uy * f
        for rid in ids:
            dx, dy = disp[rid]
            dl = math.hypot(dx, dy) or 1e-4
            pos[rid][0] += (dx / dl) * min(dl, temp)
            pos[rid][1] += (dy / dl) * min(dl, temp)
            pos[rid][0] = min(1 - MARGIN, max(MARGIN, pos[rid][0]))
            pos[rid][1] = min(1 - MARGIN, max(MARGIN, pos[rid][1]))
        temp = max(0.008, temp * 0.985)
    return {rid: (round(pos[rid][0] * CANVAS_W), round(pos[rid][1] * CANVAS_H)) for rid in ids}


def build_world(cart_path: str) -> dict | None:
    parts = cart_path.split(os.sep)
    pack = parts[-4]
    world = parts[-2]
    wdir = os.path.dirname(cart_path)
    pack_dir = os.path.join(REPO, "genre_packs", pack)

    carto = _load_yaml(cart_path)
    regions = carto.get("regions") or {}
    if not regions:
        return None
    ids = list(regions.keys())
    names = {rid: (regions[rid].get("name") or rid) for rid in ids}
    adjacency = {rid: list(regions[rid].get("adjacent") or []) for rid in ids}

    world_cfg = _load_yaml(os.path.join(wdir, "world.yaml"))
    display = world_cfg.get("name") or world.replace("_", " ").title()
    draft = bool(world_cfg.get("draft"))
    ruleset = _pack_ruleset(pack_dir)

    map_path = os.path.join(wdir, "map.yaml")
    has_raster = False
    provenance = {}
    style_hints = {"faction_layer": "default", "routes": "default"}
    image = f"{world}_map.jpg"
    header: list[str] = []
    anchors: dict[str, tuple[int, int]] = {}

    if os.path.exists(map_path):
        mp = _load_yaml(map_path)
        header = _leading_comment(map_path)
        if mp.get("treatment") == "raster":
            has_raster = True
        provenance = mp.get("provenance") or {}
        style_hints = mp.get("style_hints") or style_hints
        image = mp.get("image") or image
        raw = mp.get("node_anchors") or {}
        for rid, xy in raw.items():
            if isinstance(xy, list) and len(xy) == 2:
                anchors[rid] = (int(xy[0]), int(xy[1]))

    if not header:
        header = [f"# {display} main-map treatment (spec §2 A1). TODO: name the PD scan."]
    if not provenance:
        provenance = {
            "source": "TODO — name the public-domain scan",
            "date": "TODO",
            "archive": "TODO — archive / collection",
            "pd_basis": "TODO — confirm the public-domain basis before sourcing",
        }

    # Fill any missing anchors (new world, or a region added since map.yaml) via layout.
    missing = [rid for rid in ids if rid not in anchors]
    if missing:
        edges = set()
        for rid in ids:
            for a in adjacency[rid]:
                if a in names:
                    edges.add(tuple(sorted((rid, a))))
        laid = spring_layout(ids, edges)
        for rid in missing:
            anchors[rid] = laid.get(rid, (CANVAS_W // 2, CANVAS_H // 2))

    nodes = [
        {"id": rid, "name": names[rid], "xy": [anchors[rid][0], anchors[rid][1]],
         "adjacent": [a for a in adjacency[rid] if a in names]}
        for rid in ids
    ]
    rel = os.path.relpath(map_path, REPO)
    return {
        "pack": pack, "display": display, "ruleset": ruleset, "draft": draft,
        "hasRaster": has_raster, "path": rel, "image": image,
        "provenance": provenance, "style_hints": style_hints,
        "header": header, "canvas": [CANVAS_W, CANVAS_H], "nodes": nodes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", default=datetime.date.today().isoformat(),
                    help="build date stamped into the tool (default: today)")
    args = ap.parse_args()

    pattern = os.path.join(REPO, "genre_packs", "*", "worlds", "*", "cartography.yaml")
    worlds: dict[str, dict] = {}
    for cf in sorted(glob.glob(pattern)):
        w = build_world(cf)
        if w is None:
            continue
        key = f"{w['pack']}__{os.path.basename(os.path.dirname(cf))}"
        worlds[key] = w

    if not worlds:
        print("No worlds with cartography.yaml found — nothing to build.", file=sys.stderr)
        return 1

    with open(TEMPLATE, encoding="utf-8") as fh:
        html = fh.read()
    if "__DATA__" not in html or "__GENMETA__" not in html:
        print("Template is missing __DATA__/__GENMETA__ placeholders.", file=sys.stderr)
        return 1

    genmeta = {"generated": args.date, "worldCount": len(worlds)}
    html = html.replace("const DATA = __DATA__;", "const DATA = " + json.dumps(worlds, ensure_ascii=False) + ";")
    html = html.replace("const GENMETA = __GENMETA__;", "const GENMETA = " + json.dumps(genmeta, ensure_ascii=False) + ";")
    if "__DATA__" in html or "__GENMETA__" in html:
        print("Placeholder substitution failed.", file=sys.stderr)
        return 1

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    raster = sum(1 for w in worlds.values() if w["hasRaster"])
    print(f"Wrote {os.path.relpath(OUT, REPO)}")
    print(f"  {len(worlds)} worlds  ({raster} with a raster map.yaml, {len(worlds) - raster} auto-laid-out)")
    for key, w in worlds.items():
        flag = "raster" if w["hasRaster"] else "  new "
        print(f"    [{flag}] {key:38} {len(w['nodes']):>2} regions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

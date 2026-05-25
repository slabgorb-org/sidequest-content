"""Split legends.yaml into legends/{slug}.yaml files.

Handles both formats:
  - YAML list of legend dicts (Vec<Legend>)
  - YAML map with a "legends" key containing a list
"""
import sys
from pathlib import Path
import yaml

world_dir = Path(sys.argv[1])
src = world_dir / "legends.yaml"
dst = world_dir / "legends"

with src.open() as f:
    raw = yaml.safe_load(f)

legends = []
if isinstance(raw, list):
    legends = raw
elif isinstance(raw, dict) and "legends" in raw:
    legends = raw["legends"]
    # Save any top-level keys other than "legends" into _meta.yaml
    meta = {k: v for k, v in raw.items() if k != "legends"}
    if meta:
        dst.mkdir(exist_ok=True)
        meta_out = dst / "_meta.yaml"
        with meta_out.open("w") as f:
            yaml.dump(meta, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        print(f"  wrote {meta_out}")
elif raw is None or raw == {}:
    print(f"SKIP {src}: empty or null")
    dst.mkdir(exist_ok=True)
    src.unlink()
    print(f"  removed {src} (was empty, dir created)")
    sys.exit(0)
else:
    print(f"SKIP {src}: unrecognized format (type={type(raw).__name__})")
    sys.exit(0)

if not legends:
    print(f"SKIP {src}: no legends found")
    dst.mkdir(exist_ok=True)
    src.unlink()
    print(f"  removed {src} (was empty, dir created)")
    sys.exit(0)

dst.mkdir(exist_ok=True)
for legend in legends:
    if isinstance(legend, dict):
        title = legend.get("title", legend.get("name", legend.get("id", "unknown")))
    else:
        title = str(legend)
    slug = title.lower().replace(" ", "_").replace("-", "_").replace("'", "").replace(":", "")
    # Truncate long slugs
    slug = slug[:60]
    out = dst / f"{slug}.yaml"
    # Handle duplicates
    counter = 2
    while out.exists():
        out = dst / f"{slug}_{counter}.yaml"
        counter += 1
    with out.open("w") as f:
        yaml.dump(legend, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"  wrote {out}")

src.unlink()
print(f"  removed {src}")

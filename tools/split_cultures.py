"""Split cultures.yaml (YAML list) into cultures/{slug}.yaml files."""
import sys
from pathlib import Path
import yaml

world_dir = Path(sys.argv[1])
src = world_dir / "cultures.yaml"
dst = world_dir / "cultures"

with src.open() as f:
    data = yaml.safe_load(f)

if not isinstance(data, list):
    print(f"SKIP {src}: not a list (type={type(data).__name__})")
    sys.exit(0)

dst.mkdir(exist_ok=True)
for culture in data:
    name = culture.get("name", culture.get("id", "unknown"))
    slug = name.lower().replace(" ", "_").replace("-", "_").replace("'", "")
    out = dst / f"{slug}.yaml"
    with out.open("w") as f:
        yaml.dump(culture, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    print(f"  wrote {out}")

src.unlink()
print(f"  removed {src}")

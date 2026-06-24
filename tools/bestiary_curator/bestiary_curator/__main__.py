"""Enable ``python -m bestiary_curator <world_dir>``."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())

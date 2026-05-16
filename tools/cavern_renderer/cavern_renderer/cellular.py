"""Re-export shim — canonical cellular now lives in sidequest-server.

Spec §8 (Beneath Sünden): single generator, no fork. This module
keeps the historical import path (`cavern_renderer.cellular`) working
while delegating to sidequest.dungeon.interiors.cellular.
"""

from sidequest.dungeon.interiors.cellular import gen_cave
from sidequest.dungeon.interiors.grid import FLOOR, WALL

__all__ = ["gen_cave", "FLOOR", "WALL"]

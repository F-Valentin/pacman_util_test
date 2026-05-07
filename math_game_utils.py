from __future__ import annotations
import math


class Vec2:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

    def distance_to(self, other: Vec2) -> float:
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

from __future__ import annotations
import math


class Vec2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def distance_to(self, other: Vec2) -> float:
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def normalize(self) -> Vec2:
        return self.__truediv__(self.length())

    def length(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other: Vec2) -> Vec2:
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vec2) -> Vec2:
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vec2:
        return Vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar: float) -> Vec2:
        """__truediv__ can raise a ZeroDivisionError"""

        return Vec2(self.x / scalar, self.y / scalar)

    def __str__(self) -> str:
        return f"Vec2(x: {self.x}, y: {self.y})"

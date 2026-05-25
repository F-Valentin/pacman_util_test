import arcade
from dataclasses import dataclass


@dataclass
class Pacgum:
    x: int
    y: int
    alive: bool
    radius: float
    point: int
    color: tuple[int, int, int, int]


def draw_pacgum(pacgum: Pacgum) -> None:
    arcade.draw_circle_filled(pacgum.x, pacgum.y, pacgum.radius, pacgum.color)

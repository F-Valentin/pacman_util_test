import arcade
from dataclasses import dataclass


@dataclass
class Pacgum:
    """Simple data container for edible pacgum objects in the maze."""
    x: int
    y: int
    visible: bool
    radius: float
    point: int
    color: tuple[int, int, int, int]
    is_super: bool


def draw_pacgum(pacgum: Pacgum) -> None:
    """Render one visible pacgum as a filled circle."""
    arcade.draw_circle_filled(pacgum.x, pacgum.y, pacgum.radius, pacgum.color)

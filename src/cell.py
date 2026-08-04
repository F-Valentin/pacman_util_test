
from enum import IntEnum

import arcade

from pacgum import Pacgum


class Walls(IntEnum):
    NORTH = 0b0001
    EAST = 0b0010
    SOUTH = 0b0100
    WEST = 0b1000


class Cell:
    """Represent one tile in the maze grid, including its walls and pacgum."""

    def __init__(self, grid_pos: arcade.Vec2, walls: int, size: int) -> None:
        self._grid_x: float = grid_pos.x
        self._grid_y: float = grid_pos.y
        self._size = size
        self._walls = walls
        self.pacgum: Pacgum | None = None
        self.center: arcade.Vec2

        x = grid_pos.x
        y = grid_pos.y

        self.neighbors: list[tuple[float, float]] = [
            (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

    @property
    def grid_x(self) -> float:
        return self._grid_x

    @property
    def grid_y(self) -> float:
        return self._grid_y

    @property
    def size(self) -> int:
        return self._size

    @property
    def walls(self) -> int:
        return self._walls

    def set_pacgum(
        self,
        radius: float,
        color: tuple[int, int, int, int] = arcade.color.YELLOW_ORANGE
    ) -> None:
        """Update the pacgum radius and color for this cell."""
        function_name: str = "set_pacgum"

        if not isinstance(radius, float):
            raise TypeError(
                f"[Error] in {function_name}: "
                "radius must be a float"
            )

        if self.pacgum:
            self.pacgum.radius = radius
            self.pacgum.color = color

    def hide_pacgum(self) -> None:
        """Hide the pacgum when the player eats it."""
        if not self.pacgum:
            raise ValueError("Trying to hide a pacgum, but the pacgum is None")

        self.pacgum.visible = False

    def has_pacgum(self) -> bool:
        """Return whether this cell still has a visible pacgum."""
        if not self.pacgum:
            return False

        return self.pacgum.visible

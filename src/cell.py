import arcade
from typing import Optional
from pacgum import Pacgum


class Cell:
    def __init__(self, grid_pos: arcade.Vec2, walls: int, size: int) -> None:
        self._grid_x: float = grid_pos.x
        self._grid_y: float = grid_pos.y
        self._size = size
        self._walls = walls
        self.pacgum: Optional[Pacgum] = None
        self.center: Optional[arcade.Vec2] = None

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

    def add_pacgum(self, pacgum: Pacgum) -> None:
        function_name = "add_pacgum"

        if not isinstance(pacgum, Pacgum):
            raise ValueError(
                f"[Error] in {function_name}: pacgum must be a Pacgum type")

        self.pacgum = pacgum

    def set_pacgum(
        self,
        radius: float,
        color: tuple[int, int, int, int] = arcade.color.YELLOW_ORANGE
    ) -> None:
        function_name: str = "set_pacgum"

        if not isinstance(radius, float):
            raise ValueError(
                f"[Error] in {function_name}: "
                "radius must be a float"
            )

        if not isinstance(color, tuple):
            raise ValueError(
                f"[Error] in {function_name}: "
                "color must be a tuple[int, int, int, int]"
            )

        if self.pacgum:
            self.pacgum.radius = radius

    def has_pacgum(self) -> bool:
        if not self.pacgum:
            return False

        return self.pacgum.alive

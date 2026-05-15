from __future__ import annotations
from typing import TYPE_CHECKING

import arcade

if TYPE_CHECKING:
    from cell import Cell

class Maze:
    def __init__(self, maze: list[list[Cell]],
                 size: tuple[float, float], top_left_coord: tuple[float, float]) -> None:
        self._grid = maze
        self._width = size[0]
        self._height = size[1]
        self._offset_x: float = top_left_coord[0]
        self._offset_y: float = top_left_coord[1]
        self._tile_size: int = 50
        self._wall_points = self._build_wall_points()

    @property
    def grid(self) -> list[list[Cell]]:
        return self._grid

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    @property
    def offset_x(self) -> float:
        return self._offset_x

    @property
    def offset_y(self) -> float:
        return self._offset_y

    @property
    def tile_size(self) -> int:
        return self._tile_size

    def _build_wall_points(self) -> list[tuple[float, float]]:
        wall_points: list[tuple[float, float]] = []
        tile_size = self.tile_size
        for row in self.grid:
            for cell in row:
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.height - 1 - cell.y) * tile_size + self.offset_y
                )
                top_left = (screen_x, screen_y + tile_size)
                top_right = (screen_x + tile_size, screen_y + tile_size)
                bottom_left = (screen_x, screen_y)
                bottom_right = (screen_x + tile_size, screen_y)
                if cell.walls & 0b0001:
                    wall_points += [top_left, top_right]
                if cell.walls & 0b0010:
                    wall_points += [top_right, bottom_right]
                if cell.walls & 0b0100:
                    wall_points += [bottom_left, bottom_right]
                if cell.walls & 0b1000:
                    wall_points += [top_left, bottom_left]
        return wall_points

    def _draw_walls(self) -> None:
        arcade.draw_lines(self._wall_points, arcade.color.BLUE, 2)

    def _draw_pacgums(self) -> None:
        tile_size = self.tile_size
        for row in self.grid:
            for cell in row:
                if not cell.has_pacgum:
                    continue
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.height - 1 - cell.y) * tile_size + self.offset_y
                )
                arcade.draw_circle_filled(screen_x + tile_size // 2,
                                          screen_y + tile_size // 2,
                                          3, arcade.color.WHITE)

    def draw(self):
        self._draw_walls()
        self._draw_pacgums()

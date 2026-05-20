from __future__ import annotations
from typing import TYPE_CHECKING
import arcade

if TYPE_CHECKING:
    from maze.cell import Cell


class Maze:
    def __init__(self, maze: list[list[Cell]],
                 size: tuple[float, float],
                 top_left_coord: tuple[float, float],
                 tile_size: int) -> None:
        self._grid = maze
        self._width: float = size[0]
        self._height: float = size[1]
        self._offset_x: float = top_left_coord[0]
        self._offset_y: float = top_left_coord[1]
        self._tile_size: int = tile_size
        self._wall_points: list[tuple[float, float]
                                ] = self._build_wall_points()
        self._setup_cells()
        self.nb_of_pacgum = self._get_nb_of_pacgum()
        self._subscribe_to_its_cells()

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

    def on_pacgum_eaten(self):
        self.nb_of_pacgum -= 1

    def _subscribe_to_its_cells(self):
        for row in self.grid:
            for cell in row:
                cell.add_subscriber(self)

    def _setup_cells(self) -> None:
        tile_size = self.tile_size
        for row in self.grid:
            for cell in row:
                cell.center = (
                    int(self.offset_x + cell.x *
                        tile_size + tile_size // 2),
                    int(self.offset_y
                        + (self.height - 1 - cell.y) * tile_size
                        + tile_size // 2),
                )
                cell.has_pacgum = cell.walls != 0x0F
    # TODO
    # def remove_pacgum_at_entity_pos():
    #     pass

    def _get_nb_of_pacgum(self) -> int:
        nb_of_pacgum = 0

        for row in self.grid:
            for cell in row:
                if cell.has_pacgum:
                    nb_of_pacgum += 1

        return nb_of_pacgum

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
                if not cell.has_pacgum and not cell.has_super_pacgum:
                    continue
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.height - 1 - cell.y) * tile_size + self.offset_y
                )
                if cell.has_super_pacgum:
                    arcade.draw_circle_filled(screen_x + tile_size // 2,
                                              screen_y + tile_size // 2,
                                              10, arcade.color.WHITE)
                else:
                    arcade.draw_circle_filled(screen_x + tile_size // 2,
                                              screen_y + tile_size // 2,
                                              3, arcade.color.WHITE)

    def draw(self) -> None:
        self._draw_walls()
        self._draw_pacgums()

from __future__ import annotations
from typing import TYPE_CHECKING

import arcade

from game_seting import GameSettings

if TYPE_CHECKING:
    from cell import MazeCell


class Maze:
    def __init__(self, maze: list[list[MazeCell]],
                 size: tuple[int, int]) -> None:
        self.maze = maze
        self.width = size[0]
        self.height = size[1]


class MazeRenderer:
    def __init__(self, maze: list[list[MazeCell]], settings: GameSettings,
                 offset_x: int, offset_y: int, maze_h: int) -> None:

        self.maze = maze
        self.settings = settings
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.maze_h = maze_h
        self._wall_points = self._build_wall_points()

    def _build_wall_points(self) -> list[tuple[float, float]]:
        wall_points: list[tuple[float, float]] = []
        tile_size = self.settings.tile_size
        for row in self.maze:
            for cell in row:
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.maze_h - 1 - cell.y) * tile_size + self.offset_y
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

    def draw_walls(self) -> None:
        arcade.draw_lines(self._wall_points, arcade.color.BLUE, 2)

    def draw_pacgums(self) -> None:
        tile_size = self.settings.tile_size
        for row in self.maze:
            for cell in row:
                if not cell.has_pacgum:
                    continue
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.maze_h - 1 - cell.y) * tile_size + self.offset_y
                )
                arcade.draw_circle_filled(screen_x + tile_size // 2,
                                          screen_y + tile_size // 2,
                                          3, arcade.color.WHITE)

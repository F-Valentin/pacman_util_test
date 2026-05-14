from __future__ import annotations
from typing import TYPE_CHECKING

import arcade

from game_seting import GameSettings

if TYPE_CHECKING:
    from cell import Cell


class Maze:
    def __init__(self, maze: list[list[Cell]],
                 size: tuple[int, int]) -> None:
        self.maze = maze
        self.width = size[0]
        self.height = size[1]


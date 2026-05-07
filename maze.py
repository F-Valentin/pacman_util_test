from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cell import MazeCell


class Maze:
    def __init__(self, maze: list[list[MazeCell]], size: tuple[int, int]) -> None:
        self.maze = maze
        self.width = size[0]
        self.height = size[1]
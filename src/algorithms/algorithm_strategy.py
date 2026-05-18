from abc import ABC, abstractmethod
from maze.cell import Cell
from maze.maze import Maze


class PathfindingStrategy(ABC):
    @abstractmethod
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass


class DFSStrategy(PathfindingStrategy):

    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass

from abc import ABC, abstractmethod
from cell import Cell
from maze import Maze


class PathfindingStrategy(ABC):
    # @abstractmethod
    # def find_paths(self, start: Cell, dest: Cell,
    #                maze: Maze) -> list[list[Cell]] | None:
    #     pass

    @abstractmethod
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass


class DFSStrategy(PathfindingStrategy):
    # first problem the ghost can go to a place where the player is not present
    # second the player is not a Cell, perhaps we will a field maze_pos
    # to the player
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass


class BFSStrategy(PathfindingStrategy):
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass

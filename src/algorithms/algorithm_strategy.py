from abc import ABC, abstractmethod
from maze.cell import Cell
from maze.maze import Maze
from player.player import Player


class PathfindingStrategy(ABC):
    @abstractmethod
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass


class DFSStrategy(PathfindingStrategy):
    def __init__(self, player: Player,
                 maze: Maze):
        self.player = player
        self.maze = maze

    def find_path(self, start: Cell, dest: Cell) -> list[Cell] | None:
        print("test")

from abc import ABC, abstractmethod
from cell import Cell

class PathfindingStrategy(ABC):
    @abstractmethod
    def find_paths(self, start: Cell, dest: Cell) -> list[list[Cell]] | None:
        pass

class DFSStrategy(PathfindingStrategy):
    def find_paths(self, start: Cell, dest: Cell) -> list[list[Cell]] | None:
        pass

class BFSStrategy(PathfindingStrategy):
    def find_paths(self, start: Cell, dest: Cell) -> list[list[Cell]] | None:
        pass
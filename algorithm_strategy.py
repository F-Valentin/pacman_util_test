from abc import ABC, abstractmethod
from cell import Cell
from maze import Maze


class PathfindingStrategy(ABC):
    @abstractmethod
    def find_paths(self, start: Cell, dest: Cell,
                   maze: Maze) -> list[list[Cell]] | None:
        pass

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
        final_path: list[Cell] = []
        curr_path: list[Cell] = []
        queue: list[Cell] = []

        queue.append(start)
        while queue:
            curr_cell: Cell = queue.pop()
            if curr_cell.has_visited:
                continue

            curr_path.append(curr_cell)

            if (curr_cell.x, curr_cell.y) == (dest.x, dest.y):
                final_path = curr_path.copy()
                continue

            curr_cell.has_visited = True

            neighbors: list[Cell] | None = (
                curr_cell.get_valid_path_neighbors(maze))

            if neighbors is None:
                continue

            for neighbor in neighbors:
                if not neighbor.has_visited:
                    queue.append(neighbor)

        return final_path


class BFSStrategy(PathfindingStrategy):
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass

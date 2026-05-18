from abc import ABC, abstractmethod
from maze.cell import Cell
from maze.maze import Maze
from collections import deque
from player.player import Player
from typing import Optional


class PathfindingStrategy(ABC):
    @abstractmethod
    def find_path(self, start: Cell, dest: Cell,
                  maze: Maze) -> list[Cell] | None:
        pass


class BFSStrategy(PathfindingStrategy):
    def __init__(self, player: Player,
                 maze: Maze):
        self.player = player
        self.maze = maze

    def _get_valid_neighbors(self, x: int, y: int) -> Optional[list[Cell]]:

        north, south, east, west = 0b0001, 0b0100, 0b0010, 0b1000
        cell = self.maze.grid[y][x]

        def is_open(n_x: int, n_y: int) -> bool:
            if not (0 <= n_x < self.maze.width and 0 <= n_y < self.maze.height):
                return False
            n_cell = self.maze.grid[n_y][n_x]
            if n_cell.has_visited:
                return False
            if y + 1 == n_y and not n_cell.walls & north:
                return True
            if y - 1 == n_y and not n_cell.walls & south:
                return True
            if x + 1 == n_x and not n_cell.walls & west:
                return True
            if x - 1 == n_x and not n_cell.walls & east:
                return True
            return False

        valid_coords = filter(lambda c: is_open(c[0], c[1]), cell.neighbors)
        neighbors = [self.maze.grid[c[1]][c[0]] for c in valid_coords]
        return neighbors if neighbors else None

    def _bfs(self, start: Cell) -> tuple[tuple[int, int],
                                         dict[tuple[int, int], Cell],
                                         dict[tuple[int, int],
                                              tuple[int, int] | None]]:
        start_cord = (start.x, start.y)
        dest_cord = (self.player.actual_cell.x, self.player.actual_cell.y)

        queue = deque([start])

        came_from: dict[tuple[int, int],
                        tuple[int, int] | None] = {start_cord: None}
        cell_registry: dict[tuple[int, int], Cell] = {start_cord: start}

        while queue:
            curr_cell = queue.popleft()
            curr_cord = (curr_cell.x, curr_cell.y)

            if curr_cord == dest_cord:
                return dest_cord, cell_registry, came_from

            neighbors = self._get_valid_neighbors(curr_cell.x, curr_cell.y)

            if not neighbors:
                continue

            for neighbor in neighbors:
                neighbor_cord = (neighbor.x, neighbor.y)

                if neighbor_cord not in came_from:

                    came_from[neighbor_cord] = curr_cord
                    cell_registry[neighbor_cord] = neighbor
                    queue.append(neighbor)

    def find_path(self, start: Cell) -> list[Cell] | None:

        dest_cord, cell_registry, came_from = self._bfs(start)
        path = []
        curr = dest_cord

        while curr is not None:
            path.append(cell_registry[curr])
            curr = came_from[curr]

        path.reverse()
        return path

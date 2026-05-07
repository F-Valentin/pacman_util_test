from maze import Maze

class MazeCell:
    """MazeCellule class used to create better coordinate system."""

    def __init__(self, x: int, y: int, walls: int, size: tuple[int, int],
                 has_visited: bool):
        self.x: int = x
        self.y: int = y
        self.size: tuple[int, int] = size
        self.walls: int = walls
        self.has_visited: bool = has_visited
        self.neighbors: list[tuple[int, int]] = [
            (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

    def get_valid_path_neighbors(self, 
                                   maze: Maze) -> list[MazeCell] | None:
        """get valid path neighbor"""
        north, south, east, west = 0b0001, 0b0100, 0b0010, 0b1000
        maze_grid = maze.maze

        def is_open(n_x: int, n_y: int) -> bool:
            if not (0 <= n_x < maze.width and 0 <= n_y < maze.height):
                return False

            n_cell = maze_grid[n_y][n_x]

            if n_cell.has_visited:
                return False
            if self.y + 1 == n_y and not n_cell.walls & north:
                return True
            if self.y - 1 == n_y and not n_cell.walls & south:
                return True
            if self.x + 1 == n_x and not n_cell.walls & west:
                return True
            if self.x - 1 == n_x and not n_cell.walls & east:
                return True
            return False

        valid_coords = filter(lambda c: is_open(c[0], c[1]), self.neighbors)
        neighbors = [maze_grid[c[1]][c[0]] for c in valid_coords]

        return neighbors if neighbors else None

    def __str__(self) -> str:
        return f"cell pos: ({self.x}, {self.y})"
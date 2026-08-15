import math

import arcade
from arcade import Vec2

from cell import Cell, Walls
from mazegenerator import MazeGenerator
from pacgum import Pacgum, draw_pacgum


class MazeGenerationError(Exception):
    """Raised when the assigned A-Maze-ing package fails to build a maze."""


class Maze:
    """Build and draw a maze grid with pacgums and wall geometry."""

    def __init__(self, width: int, height: int,
                 bottom_left_pos: Vec2, cell_size: int,
                 seed: int = 0) -> None:
        """
            Build a maze.

            seed: passed straight through to the assigned A-Maze-ing
            package. A value > 0 produces a reproducible maze
            (used for the first level); 0 produces a random maze
            (used for every subsequent level).
        """
        self._grid: list[list[Cell]] = []
        self._width = width
        self._height = height
        self._bottom_left_pos = bottom_left_pos
        self._cell_size = cell_size
        self._seed = seed
        self._wall_points: list[tuple[float, float]] = []
        self._pacgums: list[Pacgum] = []
        self._nb_of_pacgums_visible = 0

        self._init_grid()

        self._wall_points = self._build_wall_points()
        self._setup_cells()
        self._pacgums = self._get_cells_pacgums()
        self._nb_of_pacgums_visible = len(self._pacgums)

    @property
    def grid(self) -> list[list[Cell]]:
        return self._grid

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def bottom_left_pos(self) -> Vec2:
        return self._bottom_left_pos

    @property
    def cell_size(self) -> int:
        return self._cell_size

    def pacgum_eaten(self) -> None:
        """
            Decrease the visible pacgum counter
            after the player consumes one.
        """
        if self._nb_of_pacgums_visible > 0:
            self._nb_of_pacgums_visible -= 1

    def _init_grid(self) -> None:
        try:
            maze_generator = MazeGenerator(
                (self.width, self.height),
                perfect=False,
                seed=self._seed,
            )
        except Exception as e:
            raise MazeGenerationError(
                "The maze generator failed to build a "
                f"{self.width}x{self.height} maze "
                f"(seed={self._seed}): {e}"
            ) from e

        grid: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            grid.append([])
            for (x, col) in enumerate(row):
                grid[y].append(Cell(Vec2(x, y), col, self._cell_size))

        self._grid = grid

    def _build_wall_points(self) -> list[tuple[float, float]]:
        wall_points: list[tuple[float, float]] = []
        cell_size: int = self._cell_size

        for cells in self.grid:
            for cell in cells:
                point_x = cell.grid_x * cell_size + self.bottom_left_pos.x

                point_y = (
                    (self.height - 1.0 - cell.grid_y) * cell_size +
                    self.bottom_left_pos.y
                )

                top_left = (point_x, point_y + cell_size)
                top_right = (point_x + cell_size, point_y + cell_size)
                bottom_left = (point_x, point_y)
                bottom_right = (point_x + cell_size, point_y)

                if cell.walls & Walls.NORTH:
                    wall_points += [top_left, top_right]
                if cell.walls & Walls.EAST:
                    wall_points += [top_right, bottom_right]
                if cell.walls & Walls.SOUTH:
                    wall_points += [bottom_left, bottom_right]
                if cell.walls & Walls.WEST:
                    wall_points += [top_left, bottom_left]

        return wall_points

    def _setup_cells(self) -> None:
        cell_size: int = self._cell_size

        point_par_pacgum = 5
        point_par_super_pacgum = 10

        blocked: int = 0x0F
        corner = [(0, 0),
                  (0, (len(self._grid) - 1)),
                  ((len(self._grid) - 1), 0),
                  ((len(self._grid) - 1), (len(self._grid) - 1))]

        pacgum_radius: float = 3.0
        super_pacgum_radius: float = 6.0
        pacgum_color: tuple[int, int, int, int] = arcade.color.WHITE
        super_pacgum_color: tuple[int, int, int, int] = arcade.color.BLUE
        pacgum_point: int = point_par_pacgum
        super_pacgum_point: int = point_par_super_pacgum

        for cells in self.grid:
            for cell in cells:
                center_x: int = int(
                    cell.grid_x * cell_size +
                    self.bottom_left_pos.x + cell_size // 2
                )

                center_y: int = int(
                    (self.height - 1 - cell.grid_y) * cell_size +
                    self.bottom_left_pos.y + cell_size // 2)

                cell.center = Vec2(center_x, center_y)

                if (cell._grid_x, cell._grid_y) in corner:
                    super_pacgum = Pacgum(
                        center_x, center_y,
                        True, super_pacgum_radius, super_pacgum_point,
                        super_pacgum_color, True
                    )

                    cell.pacgum = super_pacgum

                elif cell.walls != blocked:
                    pacgum = Pacgum(
                        center_x, center_y,
                        True, pacgum_radius, pacgum_point, pacgum_color, False
                    )

                    cell.pacgum = pacgum

    def get_valid_cell_neighbors(self, cell: Cell) -> list[Cell] | None:
        def is_open(n_x: int, n_y: int) -> bool:
            if not (
                    0 <= n_x < self.width and 0 <= n_y < self.height
            ):
                return False

            n_cell = self.get_cell(n_x, n_y)

            if cell.grid_y + 1 == n_y and not n_cell.walls & Walls.NORTH:
                return True
            if cell.grid_y - 1 == n_y and not n_cell.walls & Walls.SOUTH:
                return True
            if cell.grid_x + 1 == n_x and not n_cell.walls & Walls.WEST:
                return True
            if cell.grid_x - 1 == n_x and not n_cell.walls & Walls.EAST:
                return True

            return False

        valid_coords = filter(lambda c: is_open(int(c[0]), int(c[1])),
                              cell.neighbors)
        neighbors = [self.get_cell(int(c[0]), int(c[1])) for c in valid_coords]
        return neighbors if neighbors else None

    def has_pacgums(self) -> bool:
        return self._nb_of_pacgums_visible > 0

    def get_cell(self, x: int, y: int) -> Cell:
        return self._grid[y][x]

    def _get_cells_pacgums(self) -> list[Pacgum]:
        pacgums: list[Pacgum] = []

        for cells in self.grid:
            for cell in cells:
                if cell.pacgum and cell.has_pacgum():
                    pacgums.append(cell.pacgum)

        return pacgums

    def set_pacgums(self, point_par_pacgum: int) -> None:
        for pacgum in self._pacgums:
            if not pacgum.is_super:
                pacgum.point = point_par_pacgum

    def set_super_pacgums(self, point_par_super_pacgum: int) -> None:
        self._pacgums[0].point = point_par_super_pacgum
        self._pacgums[self._width - 1].point = point_par_super_pacgum
        self._pacgums[self._height * self.width -
                      self.width].point = point_par_super_pacgum
        self._pacgums[self._height * self._width -
                      1].point = point_par_super_pacgum

    def convert_pos_to_grid(self, pos: arcade.Vec2) -> arcade.Vec2:
        cell_size: int = self.cell_size
        bottom_left_pos = self.bottom_left_pos

        x: float = (pos.x - bottom_left_pos.x) / float(cell_size)
        y: float = ((self.height - 1)
                    - (pos.y - bottom_left_pos.y)) / float(cell_size)

        return arcade.Vec2(
            math.floor(x),
            math.floor(y)
        )

    def convert_pos_to_cell(self, pos: arcade.Vec2) -> Cell:
        grid_pos = self.convert_pos_to_grid(pos)

        return self.get_cell(int(grid_pos.x), int(grid_pos.y))

    def _draw_pacgums(self) -> None:
        for pacgum in self._pacgums:
            if pacgum.visible:
                draw_pacgum(pacgum)

    def _draw_wall_points(self) -> None:
        arcade.draw_lines(self._wall_points, arcade.color.BLUE, 2)

    def draw(self) -> None:
        self._draw_wall_points()
        self._draw_pacgums()

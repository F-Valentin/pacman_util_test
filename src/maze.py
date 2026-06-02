from typing import Optional

import arcade
from arcade import Vec2
from cell import Cell
from pacgum import Pacgum, draw_pacgum
from mazegenerator import MazeGenerator


class Maze:
    def __init__(self, width: int, height: int,
                 bottom_left_pos: Vec2, cell_size: int) -> None:
        self._grid: list[list[Cell]] = []
        self._width = width
        self._height = height
        self._bottom_left_pos = bottom_left_pos
        self._cell_size = cell_size
        self._wall_points: list[tuple[float, float]] = []
        self._pacgums: list[Pacgum] = []
        self._nb_of_pacgums_visible = 0

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
        if self._nb_of_pacgums_visible > 0:
            self._nb_of_pacgums_visible -= 1

    def setup(self, point_par_pacgum: int) -> None:
        maze_generator = MazeGenerator((self.width, self.height))
        grid: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            grid.append([])
            for (x, col) in enumerate(row):
                grid[y].append(Cell(Vec2(x, y), col, self._cell_size))

        self._grid = grid

        if self._grid:
            self._setup_cells(point_par_pacgum)
            self._wall_points = self._build_wall_points()
            self._pacgums = self._get_cells_pacgums()
            self._nb_of_pacgums_visible = len(self._pacgums)

    def _build_wall_points(self) -> list[tuple[float, float]]:
        wall_points: list[tuple[float, float]] = []
        cell_size: int = self._cell_size
        north, east, south, west = 0b0001, 0b0010, 0b0100, 0b1000

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

                if cell.walls & north:
                    wall_points += [top_left, top_right]
                if cell.walls & east:
                    wall_points += [top_right, bottom_right]
                if cell.walls & south:
                    wall_points += [bottom_left, bottom_right]
                if cell.walls & west:
                    wall_points += [top_left, bottom_left]

        return wall_points

    def _setup_cells(self, point_par_pacgum: int) -> None:
        cell_size: int = self._cell_size

        blocked: int = 0x0F

        pacgum_radius: float = 3.0
        pacgum_color: tuple[int, int, int, int] = arcade.color.WHITE
        pacgum_point: int = point_par_pacgum

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

                if cell.walls != blocked:
                    pacgum = Pacgum(
                        center_x, center_y,
                        True, pacgum_radius, pacgum_point, pacgum_color
                    )

                    cell.add_pacgum(pacgum)
    
    def _get_valid_cell_neighbors(self, cell: Cell) -> Optional[list[Cell]]:
        north, south, east, west = 0b0001, 0b0100, 0b0010, 0b1000

        def is_open(n_x: int, n_y: int) -> bool:
            if not (
                    0 <= n_x < self.width and 0 <= n_y < self.height
                    ):
                return False
            n_cell = self.get_cell(n_x, n_y)
            if cell.grid_y + 1 == n_y and not n_cell.walls & north:
                return True
            if cell.grid_y - 1 == n_y and not n_cell.walls & south:
                return True
            if cell.grid_x + 1 == n_x and not n_cell.walls & west:
                return True
            if cell.grid_x - 1 == n_x and not n_cell.walls & east:
                return True
            return False

        valid_coords = filter(lambda c: is_open(int(c[0]), int(c[1])), cell.neighbors)
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

    def _draw_pacgums(self) -> None:
        for pacgum in self._pacgums:
            if pacgum.visible:
                draw_pacgum(pacgum)

    def _draw_wall_points(self) -> None:
        arcade.draw_lines(self._wall_points, arcade.color.BLUE, 2)

    def draw(self) -> None:
        self._draw_wall_points()
        self._draw_pacgums()

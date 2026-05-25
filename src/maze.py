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
        self.__wall_points: list[tuple[float, float]] = []
        self.__pacgums: list[Pacgum] = []

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

    def setup(self) -> None:
        maze_generator = MazeGenerator((self.width, self.height))
        grid: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            grid.append([])
            for (x, col) in enumerate(row):
                grid[y].append(Cell(Vec2(x, y), col, self._cell_size))

        self._grid = grid

        if self._grid:
            self.__setup_cells()
            self.__wall_points = self.__build_wall_points()
            self.__pacgums = self.__get_cells_pacgums()

    def __build_wall_points(self) -> list[tuple[float, float]]:
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

    def __setup_cells(self) -> None:
        cell_size: int = self._cell_size

        blocked: int = 0x0F

        pacgum_radius: float = 3.0
        pacgum_color: tuple[int, int, int, int] = arcade.color.WHITE
        pacgum_point: int = 10

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
    
    def get_cell(self, x: int, y: int) -> Cell:
        return self._grid[y][x]

    def __get_cells_pacgums(self) -> list[Pacgum]:
        pacgums: list[Pacgum] = []

        for cells in self.grid:
            for cell in cells:
                if cell.pacgum and cell.has_pacgum():
                    pacgums.append(cell.pacgum)

        return pacgums

    def __draw_pacgums(self) -> None:
        for pacgum in self.__pacgums:
            if pacgum.alive:
                draw_pacgum(pacgum)

    def __draw_wall_points(self) -> None:
        arcade.draw_lines(self.__wall_points, arcade.color.BLUE, 2)

    def draw(self) -> None:
        self.__draw_wall_points()
        self.__draw_pacgums()

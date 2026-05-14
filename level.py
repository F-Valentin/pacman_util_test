import arcade

from abc import ABC, abstractmethod
from mazegenerator import MazeGenerator
from player import Player
from ghost import Ghost
from maze import Maze
from cell import Cell
from game_configuration import GameConfig
from algorithm_strategy import PathfindingStrategy
from game_seting import GameSettings

class LevelSwitcher(ABC):
    @abstractmethod
    def next_level(self) -> bool:
        pass


class MazeRenderer:
    def __init__(self, maze: list[list[Cell]], settings: GameSettings,
                 offset_x: int, offset_y: int, maze_h: int) -> None:

        self.maze = maze
        self.settings = settings
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.maze_h = maze_h
        self._wall_points = self._build_wall_points()

    def _build_wall_points(self) -> list[tuple[float, float]]:
        wall_points: list[tuple[float, float]] = []
        tile_size = self.settings.tile_size
        for row in self.maze:
            for cell in row:
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.maze_h - 1 - cell.y) * tile_size + self.offset_y
                )
                top_left = (screen_x, screen_y + tile_size)
                top_right = (screen_x + tile_size, screen_y + tile_size)
                bottom_left = (screen_x, screen_y)
                bottom_right = (screen_x + tile_size, screen_y)
                if cell.walls & 0b0001:
                    wall_points += [top_left, top_right]
                if cell.walls & 0b0010:
                    wall_points += [top_right, bottom_right]
                if cell.walls & 0b0100:
                    wall_points += [bottom_left, bottom_right]
                if cell.walls & 0b1000:
                    wall_points += [top_left, bottom_left]
        return wall_points

    def draw_walls(self) -> None:
        arcade.draw_lines(self._wall_points, arcade.color.BLUE, 2)

    def draw_pacgums(self) -> None:
        tile_size = self.settings.tile_size
        for row in self.maze:
            for cell in row:
                if not cell.has_pacgum:
                    continue
                screen_x = cell.x * tile_size + self.offset_x
                screen_y = (
                    (self.maze_h - 1 - cell.y) * tile_size + self.offset_y
                )
                arcade.draw_circle_filled(screen_x + tile_size // 2,
                                          screen_y + tile_size // 2,
                                          3, arcade.color.WHITE)


class Level(arcade.View):
    def __init__(self, player: Player, ghosts: list[Ghost], maze: Maze, maze_renderer: MazeRenderer, level_switcher: LevelSwitcher) -> None:
        self._player = player
        self._ghosts = ghosts
        self._maze = maze
        self._level_switcher = level_switcher
        self.renderer = maze_renderer
    
    def on_draw(self) -> None:
        self.window.clear()
        self.renderer.draw_walls()
        self.renderer.draw_pacgums()
        self._player.draw()

class LevelFactory:
    def __init__(self,
                 game_config: GameConfig,
                 ghost_strategy: PathfindingStrategy,
                 maze_size: tuple[int, int],
                 level_switcher: LevelSwitcher,
                 game_settings: GameSettings
                 ) -> None:
        self.nb_of_ghosts =4 
        self.ghost_strategy = ghost_strategy
        self.maze_size = maze_size
        self.game_config = game_config
        self.level_switcher = level_switcher
        self.game_settings = game_settings
    
    def _create_enemies(self):
        ghosts = []
        for _ in range(self.nb_of_ghosts):
            ghosts.append(Ghost("", self.ghost_strategy))
        return ghosts


    def create_level(self) -> Level:
        maze_generator = MazeGenerator()
        tile_size = 60
        maze: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            maze.append([])
            for (x, col) in enumerate(row):
                maze[y].append(Cell(x, y, col, (self.maze_size[0], self.maze_size[1]), False))

        maze_generator = MazeGenerator()
        maze_w: int = len(maze[0])
        maze_h: int = len(maze)
        tile_size = 60
        
        offset_x: int = (
            (self.game_settings.screen_width - maze_w * tile_size) // 2
        )

        offset_y: int = (
            (self.game_settings.screen_height - maze_h * tile_size) // 2)

        maze_renderer = MazeRenderer(maze, self.game_settings, offset_x, offset_y, maze_h)
        m = Maze(maze, self.maze_size)
        return Level(Player(), self._create_enemies(), m, maze_renderer, self.level_switcher)  


class LevelManager(LevelSwitcher):
    def __init__(self, window: arcade.Window) -> None:
        self._window = window
        self._levels: list[Level] = []
        self._current_level_idx = 0

    def append_levels(self, levels: list[Level]) -> None:
        self._levels.extend(levels)

    def next_level(self) -> bool:
        if self._current_level_idx < len(self._levels) - 1:
            self._current_level_idx += 1
            self._window.show_view(self._levels[self._current_level_idx])
            return True
        
        return False 
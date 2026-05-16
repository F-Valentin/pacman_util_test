import arcade

from abc import ABC, abstractmethod
from mazegenerator import MazeGenerator
from player import Player
from ghost import Ghost
from maze import Maze
from cell import Cell
from game_configuration import GameConfig
from algorithm_strategy import PathfindingStrategy
from view_manager import ViewManager


class LevelSwitcher(ABC):
    @abstractmethod
    def next_level(self) -> None:
        pass

# class Level(arcade.View):
#     def __init__(self,
# player: Player,
# ghosts: list[Ghost], maze: Maze, level_switcher: LevelSwitcher) -> None:
#         self._player = player
#         self._ghosts = ghosts
#         self._maze = maze
#         self._level_switcher = level_switcher

#     def on_draw(self) -> None:
#         self.window.clear()
#         self._maze.draw()
#         self._player.draw()


class Level(arcade.View):
    def __init__(self, player: Player, maze: Maze) -> None:
        super().__init__()
        self._player = player
        self._maze = maze
        self._time_accumulator: float = 0

    def on_update(self, delta_time: float) -> None:
        self._time_accumulator += delta_time
        time_step: float = 1 / 60
        while self._time_accumulator >= time_step:
            self._fixed_update(time_step)
            self._time_accumulator -= time_step

    def _fixed_update(self, dt: float) -> None:
        self._player.update(dt)
        player_pixel_x = int(self._player.sprite.center_x)
        player_pixel_y = int(self._player.sprite.center_y)

        for row in self._maze.grid:
            for cell in row:
                if cell.center != (player_pixel_x, player_pixel_y):
                    continue
                self._player.move_to_next_cell(cell)
                break

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self._player.next_direction = "UP"
        elif key in (arcade.key.DOWN, arcade.key.S):
            self._player.next_direction = "DOWN"
        elif key in (arcade.key.LEFT, arcade.key.A):
            self._player.next_direction = "LEFT"
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self._player.next_direction = "RIGHT"

    def on_draw(self) -> None:
        self.window.clear()
        self._maze.draw()
        self._player.draw()


class LevelFactory:
    def __init__(self,
                 player: Player,
                 game_config: GameConfig,
                 ghost_strategy: PathfindingStrategy,
                 maze_size: tuple[int, int],
                 level_switcher: LevelSwitcher
                 ) -> None:
        self.nb_of_ghosts = 4
        self._player = player
        self.ghost_strategy = ghost_strategy
        self.maze_size = maze_size
        self.game_config = game_config
        self.level_switcher = level_switcher

    def _create_enemies(self) -> list[Ghost]:
        ghosts = []
        for _ in range(self.nb_of_ghosts):
            ghosts.append(Ghost("", self.ghost_strategy))
        return ghosts

    def _compute_player_start(self, maze: Maze) -> tuple[int, int]:
        tile_size = maze.tile_size
        half = maze.width * tile_size // 2
        offset = 0 if maze.width % 2 != 0 else -tile_size // 2
        return (
            int(maze.offset_x + half + offset),
            int(maze.offset_y + half + offset),
        )

    def create_level(self) -> Level:
        maze_generator = MazeGenerator(self.maze_size)
        tile_size = 50
        grid: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            grid.append([])
            for (x, col) in enumerate(row):
                grid[y].append(
                    Cell(
                        x,
                        y,
                        col,
                        (self.maze_size[0],
                         self.maze_size[1]),
                        False))

        offset_x: int = (
            (self.game_config.screen_width -
             self.maze_size[0] * tile_size) // 2
        )

        offset_y: int = (
            (self.game_config.screen_height -
             self.maze_size[1] * tile_size) // 2)

        maze = Maze(grid, self.maze_size, (offset_x, offset_y))
        (p_x, p_y) = self._compute_player_start(maze)
        self._player.set_position(p_x, p_y)
        # return Level(Player(), self._create_enemies(), m,
        # self.level_switcher)
        return Level(self._player, maze)


class LevelManager(LevelSwitcher):
    def __init__(self, window: arcade.Window) -> None:
        self._window = window
        self._levels: list[Level] = []
        self._current_level_idx = 0

    def append_levels(self, levels: list[Level]) -> None:
        self._levels.extend(levels)

    def next_level(self):
        if self._current_level_idx < len(self._levels) - 1:
            self._current_level_idx += 1
            self._window.show_view(self._levels[self._current_level_idx])
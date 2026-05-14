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

# class Level(arcade.View):
#     def __init__(self, player: Player, ghosts: list[Ghost], maze: Maze, level_switcher: LevelSwitcher) -> None:
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
        self._time_accumulator = 0
    
    def _compute_player_start(self) -> tuple[int, int]:
        tile_size = self._maze.tile_size
        half = self._maze.width * tile_size // 2
        print(half)
        offset = 0 if self._maze.width % 2 != 0 else -tile_size // 2
        return (
            int(self._maze.offset_x + half + offset),
            int(self._maze.offset_y + half + offset),
        )

    def _setup_cells(self) -> None:
        tile_size = self._maze.tile_size
        for row in self._maze.grid:
            for cell in row:
                cell.center = (
                    int(self._maze.offset_x + cell.x * tile_size + tile_size // 2),
                    int(self._maze.offset_y
                    + (self._maze.height - 1 - cell.y) * tile_size
                    + tile_size // 2),
                )
                cell.has_pacgum = cell.walls != 0x0F

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
                self._handle_hub(cell)
                break

    def _handle_hub(self, cell: Cell) -> None:
        cell.has_pacgum = False
        self._player.change_x = 0.0
        self._player.change_y = 0.0
        speed = 2.5
        next_dir = self._player.next_direction

        if next_dir == "UP" and not cell.walls & 0b0001:
            self._player.sprite.angle = -90
            self._player.next_direction = None
            self._player.direction = "UP"
            self._player.change_y = speed
        elif next_dir == "DOWN" and not cell.walls & 0b0100:
            self._player.sprite.angle = 90
            self._player.next_direction = None
            self._player.direction = "DOWN"
            self._player.change_y = -speed
        elif next_dir == "RIGHT" and not cell.walls & 0b0010:
            self._player.sprite.angle = 0
            self._player.next_direction = None
            self._player.direction = "RIGHT"
            self._player.change_x = speed
        elif next_dir == "LEFT" and not cell.walls & 0b1000:
            self._player.sprite.angle = 180
            self._player.next_direction = None
            self._player.direction = "LEFT"
            self._player.change_x = -speed
        else:
            self._player.next_direction = self._player.direction

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
        maze_generator = MazeGenerator(self.maze_size)
        tile_size = 50
        maze: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            maze.append([])
            for (x, col) in enumerate(row):
                maze[y].append(Cell(x, y, col, (self.maze_size[0], self.maze_size[1]), False))

        
        offset_x: int = (
            (self.game_settings.screen_width - self.maze_size[0] * tile_size) // 2
        )

        offset_y: int = (
            (self.game_settings.screen_height - self.maze_size[1] * tile_size) // 2)

        m = Maze(maze, self.maze_size, (offset_x, offset_y))
        #return Level(Player(), self._create_enemies(), m, self.level_switcher)  
        return Level(Player(), m)


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
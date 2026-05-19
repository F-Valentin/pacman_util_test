import arcade

from abc import ABC, abstractmethod
from maze.mazegenerator import MazeGenerator
from player.player import Player
from enemy.ghost import Ghost
from maze.maze import Maze
from maze.cell import Cell
from game.game_configuration import GameConfig
from algorithms.algorithm_strategy import PathfindingStrategy, BFSStrategy
from subscriber import ILevelManagerSubscriber
from game.game_collision import check_collision

class PauseView(arcade.View):
    def __init__(self, previous_view: arcade.View):
        super().__init__()
        self._previous_view = previous_view

    def on_draw(self):
        # Draw player, for effect, on pause screen.
        # The previous View (GameView) was passed in
        # and saved in self.game_view.

        # draw an orange filter over him
        self.clear()
        self._previous_view.on_draw()
        pause = arcade.Text("PAUSED", self.window.width / 2,
                            self.window.height / 2 + 100,
                            arcade.color.WHITE,
                            font_size=50, anchor_x="center")
        pause.draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self._previous_view)


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
    def __init__(self, player: Player, maze: Maze,
                 ghosts: list[Ghost], level_switcher: LevelSwitcher) -> None:
        super().__init__()
        self._player = player
        self._maze = maze
        self._level_switcher = level_switcher

        self._ghosts: list[Ghost] = ghosts

        self._time_accumulator: float = 0
    
    def on_show_view(self) -> None:
        print("level show")
    def on_update(self, delta_time: float) -> None:
        self._time_accumulator += delta_time
        time_step: float = 1 / 60
        while self._time_accumulator >= time_step:
            if not self._maze.nb_of_pacgum:
                self._level_switcher.next_level()
                break

            self._fixed_update(time_step)
            self._time_accumulator -= time_step

    def _fixed_update(self, dt: float) -> None:

        self._player.update(dt)
        for ghost in self._ghosts:
            ghost.update(dt)

        for ghost in self._ghosts:
            ghost_pixel_x = int(ghost.sprite.center_x)
            ghost_pixel_y = int(ghost.sprite.center_y)

            if check_collision(self._player.sprite, ghost.sprite):
                self._player.lives -= 1
                if not self._player.lives:
                    self._player.die()
                self._player.restart(self._maze)
                self.restart_ghosts_pos()
                return

            for row in self._maze.grid:
                for cell in row:
                    if cell.center == (ghost_pixel_x, ghost_pixel_y):
                        ghost.actual_cell = cell
                        ghost.move_to_next_cell()
                        break

        player_pixel_x = int(self._player.sprite.center_x)
        player_pixel_y = int(self._player.sprite.center_y)

        for row in self._maze.grid:
            for cell in row:
                if cell.center != (player_pixel_x, player_pixel_y):
                    continue
                self._player.actual_cell = cell
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
        elif key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))
    
    def restart_ghosts_pos(self):
        # marche pas 
        ghost_configs = [
            {"asset": "assets/blinky.png",
             "corner": (0, 0),
             "difficulty_id": 2,
             "speed": 4},
            {"asset": "assets/pinky.png",
             "corner": (0, self._maze.width - 1),
             "difficulty_id": 8,
             "speed": 3},
            {"asset": "assets/inky.png",
             "corner": (self._maze.height - 1, 0),
             "difficulty_id": 12,
             "speed": 2.25},
            {"asset": "assets/clyde.png",
             "corner": (self._maze.height - 1, self._maze.width - 1),
             "difficulty_id": 17,
             "speed": 2.25}]

        i = 0
        for config in ghost_configs:
            y_index, x_index = config["corner"]
            cell_target = self._maze.grid[y_index][x_index]

            self._ghosts[i].set_position(cell_target.center[0], cell_target.center[1],
                               cell_target)
            self._ghosts[i].current_path = []
            self._ghosts[i].change_x = 0
            self._ghosts[i].change_y = 0
            i += 1

    def on_draw(self) -> None:
        self.window.clear()
        self._maze.draw()
        self._player.draw()
        for ghost in self._ghosts:
            ghost.draw()


class LevelFactory:
    def __init__(self,
                 player: Player,
                 game_config: GameConfig,
                 maze_size: tuple[int, int],
                 level_switcher: LevelSwitcher
                 ) -> None:
        self.nb_of_ghosts = 4
        self._player = player
        self.maze_size = maze_size
        self.game_config = game_config
        self.level_switcher = level_switcher

    def _create_enemies(self, maze: Maze) -> list[Ghost]:
        ghosts = []

        ghost_configs = [
            {"asset": "assets/blinky.png",
             "corner": (0, 0),
             "difficulty_id": 2,
             "speed": 4},
            {"asset": "assets/pinky.png",
             "corner": (0, self.maze_size[0] - 1),
             "difficulty_id": 8,
             "speed": 3},
            {"asset": "assets/inky.png",
             "corner": (self.maze_size[1] - 1, 0),
             "difficulty_id": 12,
             "speed": 2.25},
            {"asset": "assets/clyde.png",
             "corner": (self.maze_size[1] - 1, self.maze_size[0] - 1),
             "difficulty_id": 17,
             "speed": 2.25}]

        for config in ghost_configs:
            ghost = Ghost(config["asset"], BFSStrategy(self._player, maze),
                          config["difficulty_id"], config["speed"])

            y_index, x_index = config["corner"]
            cell_target = maze.grid[y_index][x_index]

            ghost.set_position(cell_target.center[0], cell_target.center[1],
                               cell_target)

            ghosts.append(ghost)

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
        tile_size = self.game_config.tile_size
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

        maze = Maze(grid, self.maze_size, (offset_x, offset_y), tile_size)
        (p_x, p_y) = self._compute_player_start(maze)
        target_cell = maze.grid[maze.height // 2][maze.width // 2]
        self._player.set_position(p_x, p_y, target_cell)

        enemies = self._create_enemies(maze)

        # return Level(Player(), self._create_enemies(), m,
        # self.level_switcher)
        return Level(self._player, maze, enemies, self.level_switcher)


class LevelManager(LevelSwitcher):
    def __init__(self, window: arcade.Window) -> None:
        self._window = window
        self._levels: list[Level] = []
        self._current_level_idx = 0
        self._subscribers: list[ILevelManagerSubscriber] = []

    def add_subscriber(self, subscriber: ILevelManagerSubscriber) -> None:
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: ILevelManagerSubscriber) -> None:
        self._subscribers.remove(subscriber)

    def append_level(self, level: Level) -> None:
        self._levels.append(level)

    def append_levels(self, levels: list[Level]) -> None:
        self._levels.extend(levels)

    def all_levels_completed(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_all_levels_completed()

    def next_level(self) -> None:
        if self._current_level_idx < len(self._levels) - 1:
            self._current_level_idx += 1
            self._window.show_view(self._levels[self._current_level_idx])
        else:
            self.all_levels_completed()

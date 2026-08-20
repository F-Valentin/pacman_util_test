"""Core game orchestration for the Pac-Man prototype."""

from typing import Any

import arcade

from button import ButtonGroup
from cheatmode import CheatMode
from entity.ghost import Ghost
from entity.player import Player
from game_configuration import GameConfig
from level import Level
from maze import Maze, MazeGenerationError
from paths import AssetLoadError
from views import EndGameView, MenuView


class Game:
    """Coordinate the main menu flow and level launch for the game."""

    LEVEL_CATALOG = [
        {
            "maze_width": 7, "maze_height": 7, "time_limit": 60,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 40, "col": 0, "row": 0, "speed": 1.5},
            ],
        },
        {
            "maze_width": 8, "maze_height": 8, "time_limit": 60,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 35, "col": 0, "row": 0, "speed": 1.5},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 38, "col": 6, "row": 6, "speed": 1.5},
            ],
        },
        {
            "maze_width": 9, "maze_height": 9, "time_limit": 75,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 28, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/pinky.png",
                 "difficulty_id": 32, "col": 8, "row": 8, "speed": 2.0},
            ],
        },
        {
            "maze_width": 9, "maze_height": 9, "time_limit": 75,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 22, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 26, "col": 8, "row": 8, "speed": 2.0},
            ],
        },
        {
            "maze_width": 9, "maze_height": 9, "time_limit": 80,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 18, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/pinky.png",
                 "difficulty_id": 22, "col": 8, "row": 8, "speed": 2.0},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 25, "col": 0, "row": 8, "speed": 2.0},
            ],
        },
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 100,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 14, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/inky.png",
                 "difficulty_id": 17, "col": 10, "row": 0, "speed": 2.5},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 20, "col": 0, "row": 10, "speed": 2.0},
            ],
        },
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 100,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 10, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/pinky.png",
                 "difficulty_id": 13, "col": 10, "row": 0, "speed": 2.0},
                {"sprite": "assets/inky.png",
                 "difficulty_id": 16, "col": 0, "row": 10, "speed": 2.0},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 19, "col": 10, "row": 10, "speed": 2.0},
            ],
        },
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 90,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 7, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/pinky.png",
                 "difficulty_id": 9, "col": 10, "row": 0, "speed": 2.0},
                {"sprite": "assets/inky.png",
                 "difficulty_id": 12, "col": 0, "row": 10, "speed": 2.0},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 15, "col": 10, "row": 10, "speed": 2.5},
            ],
        },
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 80,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 4, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/pinky.png",
                 "difficulty_id": 6, "col": 10, "row": 0, "speed": 2.0},
                {"sprite": "assets/inky.png",
                 "difficulty_id": 8, "col": 0, "row": 10, "speed": 2.5},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 10, "col": 10, "row": 10, "speed": 2.5},
            ],
        },
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 70,
            "ghosts": [
                {"sprite": "assets/blinky.png",
                 "difficulty_id": 1, "col": 0, "row": 0, "speed": 2.5},
                {"sprite": "assets/pinky.png",
                 "difficulty_id": 3, "col": 10, "row": 0, "speed": 2.0},
                {"sprite": "assets/inky.png",
                 "difficulty_id": 5, "col": 0, "row": 10, "speed": 2.5},
                {"sprite": "assets/clyde.png",
                 "difficulty_id": 7, "col": 10, "row": 10, "speed": 3.0},
            ],
        },
    ]

    def __init__(self, window: arcade.Window,
                 game_config: GameConfig) -> None:
        self._window = window
        self._game_config = game_config
        self._menu_view: MenuView
        self._button_group: ButtonGroup
        self._current_level_index: int = 0
        self.cheat_mode: CheatMode
        self.can_skip_levels = False
        self.cheat_mode_init = False
        self._player: Player

    @property
    def menu_view(self) -> MenuView:
        return self._menu_view

    def run(self) -> None:
        """Display the menu view and start the Arcade event loop."""
        self._menu_view = MenuView(self)
        self._window.show_view(self._menu_view)

        arcade.run()

    def start(self) -> None:
        """Reset progression and load the first level."""
        self.cheat_mode = CheatMode(self._window)
        self.can_skip_levels = False
        self.cheat_mode_init = False
        self._current_level_index = 0
        self.load_level(current_score=0, player_infinite_life=False)

    def load_level(self, current_score: int,
                   player_infinite_life: bool) -> None:
        """Read the catalog at the current index and build + show the level."""

        config: dict[str, Any] = self.LEVEL_CATALOG[self._current_level_index]

        maze_width: int = int(config["maze_width"])
        maze_height: int = int(config["maze_height"])
        cell_size = self._game_config.tile_size
        time_limit: int = int(config["time_limit"])

        offset_x: int = (
            (self._game_config.screen_width -
             maze_width * cell_size) // 2
        )

        offset_y: int = (
            (self._game_config.screen_height -
             maze_height * cell_size) // 2
        )

        level_seed = (
            self._game_config.seed
            if self._current_level_index == 0 else 0
        )

        try:
            maze = Maze(
                maze_width,
                maze_height,
                arcade.Vec2(
                    offset_x,
                    offset_y),
                cell_size,
                seed=level_seed,
            )
        except MazeGenerationError as e:
            print(f"[Maze Error] {e}")
            self.game_over(current_score)
            return

        maze.set_pacgums(self._game_config.points_per_pacgum)
        maze.set_super_pacgums(self._game_config.points_per_super_pacgum)

        try:
            ghosts: list[Ghost] = []
            for g in config["ghosts"]:
                position = maze.get_cell(g["col"], g["row"])
                ghost = Ghost.at_cell(
                    position,
                    self._game_config.points_per_ghost,
                    g["sprite"],
                    g["difficulty_id"],
                    g["speed"],
                    maze)
                ghosts.append(ghost)

            half = maze_width * cell_size // 2
            offset = 0 if maze_width % 2 != 0 else -cell_size // 2
            x = int(offset_x + half + offset)
            y = int(offset_y + half + offset)

            pos = arcade.Vec2(x, y)
            player = Player(
                pos,
                current_score,
                maze,
                ghosts,
                lives=self._game_config.lives
            )
        except AssetLoadError as e:
            print(f"[Asset Error] {e}")
            self.game_over(current_score)
            return

        player.infinite_life = player_infinite_life
        maze.convert_pos_to_cell(pos).hide_pacgum()

        level = Level(player, maze, ghosts, time_limit, self)

        self.cheat_mode.player_infinite_life = player.toggle_infinite_life
        self.cheat_mode.ghosts_freeze = [g.toggle_freeze for g in ghosts]

        if not self.cheat_mode_init:
            self.cheat_mode.can_skip_levels = self._skip_levels
            self.cheat_mode_init = True

        self._player = player

        self._window.show_view(level)

    def _skip_levels(self) -> None:
        self.can_skip_levels = not self.can_skip_levels

    def next_level(self, score: int) -> None:
        """Advance to the next level, or show the final victory screen."""
        self._current_level_index += 1
        if self._current_level_index < len(self.LEVEL_CATALOG):
            self.load_level(score, self._player.infinite_life)
        else:
            self._window.show_view(
                EndGameView(True, score, self._menu_view))

    def game_over(self, score: int) -> None:
        """Show the game-over screen immediately."""
        self._window.show_view(
            EndGameView(False, score, self._menu_view))

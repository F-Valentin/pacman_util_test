"""Core game orchestration for the Pac-Man prototype."""

import arcade
from level import Level
from entity.player import Player
from maze import Maze
from views import MenuView, EndGameView
from button import ButtonGroup
from entity.ghost import Ghost
from game_configuration import GameConfig


class Game:
    """Coordinate the main menu flow and level launch for the game."""

    LEVEL_CATALOG = [
        # Niveau 1 — 7×7, 1 fantôme très lent mais pas idiot
        {
            "maze_width": 7, "maze_height": 7, "time_limit": 60,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 40, "col": 0, "row": 0, "speed": 1.5},
            ],
        },
        # Niveau 2 — 7×7, 2 fantômes lents, un peu plus malins
        {
            "maze_width": 7, "maze_height": 7, "time_limit": 60,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 35, "col": 0, "row": 0, "speed": 1.5},
                {"sprite": "assets/clyde.png",  "difficulty_id": 38, "col": 6, "row": 6, "speed": 1.5},
            ],
        },
        # Niveau 3 — 9×9, vitesse monte, difficulty_id compense
        {
            "maze_width": 9, "maze_height": 9, "time_limit": 75,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 28, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/pinky.png",  "difficulty_id": 32, "col": 8, "row": 8, "speed": 2.0},
            ],
        },
        # Niveau 4 — 9×9, même vitesse, fantômes plus malins
        {
            "maze_width": 9, "maze_height": 9, "time_limit": 75,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 22, "col": 0, "row": 0, "speed": 2.0},
                {"sprite": "assets/clyde.png",  "difficulty_id": 26, "col": 8, "row": 8, "speed": 2.0},
            ],
        },
        # Niveau 5 — 9×9, 3 fantômes, vitesse monte légèrement
        {
            "maze_width": 9, "maze_height": 9, "time_limit": 80,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 18, "col": 0, "row": 0, "speed": 2.25},
                {"sprite": "assets/pinky.png",  "difficulty_id": 22, "col": 8, "row": 8, "speed": 2.0},
                {"sprite": "assets/clyde.png",  "difficulty_id": 25, "col": 0, "row": 8, "speed": 2.0},
            ],
        },
        # Niveau 6 — 11×11, vitesse stable, malin monte
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 100,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 14, "col": 0,  "row": 0,  "speed": 2.25},
                {"sprite": "assets/inky.png",   "difficulty_id": 17, "col": 10, "row": 0,  "speed": 2.25},
                {"sprite": "assets/clyde.png",  "difficulty_id": 20, "col": 0,  "row": 10, "speed": 2.0},
            ],
        },
        # Niveau 7 — 11×11, 4 fantômes, vitesse monte à 3.0
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 100,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 10, "col": 0,  "row": 0,  "speed": 3.0},
                {"sprite": "assets/pinky.png",  "difficulty_id": 13, "col": 10, "row": 0,  "speed": 2.25},
                {"sprite": "assets/inky.png",   "difficulty_id": 16, "col": 0,  "row": 10, "speed": 2.25},
                {"sprite": "assets/clyde.png",  "difficulty_id": 19, "col": 10, "row": 10, "speed": 2.0},
            ],
        },
        # Niveau 8 — 11×11, tous à 3.0 minimum, très malins
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 90,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 7,  "col": 0,  "row": 0,  "speed": 3.0},
                {"sprite": "assets/pinky.png",  "difficulty_id": 9,  "col": 10, "row": 0,  "speed": 3.0},
                {"sprite": "assets/inky.png",   "difficulty_id": 12, "col": 0,  "row": 10, "speed": 3.0},
                {"sprite": "assets/clyde.png",  "difficulty_id": 15, "col": 10, "row": 10, "speed": 2.25},
            ],
        },
        # Niveau 9 — 11×11, très rapides et très malins
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 80,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 4,  "col": 0,  "row": 0,  "speed": 3.0},
                {"sprite": "assets/pinky.png",  "difficulty_id": 6,  "col": 10, "row": 0,  "speed": 3.0},
                {"sprite": "assets/inky.png",   "difficulty_id": 8,  "col": 0,  "row": 10, "speed": 3.0},
                {"sprite": "assets/clyde.png",  "difficulty_id": 10, "col": 10, "row": 10, "speed": 3.0},
            ],
        },
        # Niveau 10 — enfer : Blinky à 4.0, les autres ultra-malins et rapides
        {
            "maze_width": 11, "maze_height": 11, "time_limit": 70,
            "ghosts": [
                {"sprite": "assets/blinky.png", "difficulty_id": 1,  "col": 0,  "row": 0,  "speed": 4.0},
                {"sprite": "assets/pinky.png",  "difficulty_id": 3,  "col": 10, "row": 0,  "speed": 3.0},
                {"sprite": "assets/inky.png",   "difficulty_id": 5,  "col": 0,  "row": 10, "speed": 3.0},
                {"sprite": "assets/clyde.png",  "difficulty_id": 7,  "col": 10, "row": 10, "speed": 3.0},
            ],
        },
    ]

    def __init__(self, window: arcade.Window, game_config: GameConfig) -> None:
        self._window = window
        self._game_config = game_config
        self._menu_view: MenuView
        self._button_group: ButtonGroup

        self._current_level_index: int = 0

    def run(self) -> None:
        """Display the menu view and start the Arcade event loop."""
        self._menu_view = MenuView(self)
        self._window.show_view(self._menu_view)

        arcade.run()

    def start(self) -> None:
        """Reset progression and load the first level."""
        self._current_level_index = 0
        self.load_level()

    def load_level(self) -> None:
        """Read the catalog at the current index and build + show the level."""

        config = self.LEVEL_CATALOG[self._current_level_index]

        maze_width = config["maze_width"]
        maze_height = config["maze_height"]
        cell_size = 72
        time_limit = config["time_limit"]

        offset_x: int = (
            (self._game_config.screen_width -
             maze_width * cell_size) // 2
        )

        offset_y: int = (
            (self._game_config.screen_height -
             maze_height * cell_size) // 2
        )

        maze = Maze(
            maze_width,
            maze_height,
            arcade.Vec2(
                offset_x,
                offset_y),
            cell_size
        )

        maze.setup(self._game_config.points_per_pacgum)

        player = Player(maze)

        half = maze_width * cell_size // 2
        offset = 0 if maze_width % 2 != 0 else -cell_size // 2
        x = int(offset_x + half + offset)
        y = int(offset_y + half + offset)

        score_ui_y = offset_y + maze_height * cell_size + 100
        hp_bar_pos = arcade.Vec2(offset_x, offset_y - 100)

        p_position = arcade.Vec2(x, y)
        score_ui_pos = arcade.Vec2(offset_x, score_ui_y)

        player.setup(
            p_position,
            score_ui_pos,
            hp_bar_pos,
            self._game_config.lives)

        ghosts: list[Ghost] = []
        for g in config["ghosts"]:
            ghost = Ghost(g["sprite"], g["difficulty_id"], g["speed"], maze, player)
            position = maze.get_cell(g["col"], g["row"])
            ghost.setup(position)
            ghosts.append(ghost)

        level = Level(player, maze, ghosts, time_limit, self)
        level.setup()
        self._window.show_view(level)

    def next_level(self, score: int) -> None:
        """Advance to the next level, or show the final victory screen."""
        self._current_level_index += 1
        if self._current_level_index < len(self.LEVEL_CATALOG):
            self.load_level()
        else:
            self._window.show_view(EndGameView(True, score, self._menu_view))

    def game_over(self, score: int) -> None:
        """Show the game-over screen immediately."""
        self._window.show_view(EndGameView(False, score, self._menu_view))

    def pause(self) -> None:
        pass

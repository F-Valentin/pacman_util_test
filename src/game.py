import arcade
from level import Level
from entity.player import Player
from maze import Maze
from typing import TYPE_CHECKING
from views import MenuView
from button import ButtonGroup
from entity.ghost import Ghost
from game_configuration import GameConfig


class Game:
    def __init__(self, window: arcade.Window, game_config: GameConfig) -> None:
        self._window = window
        self._game_config = game_config
        self._menu_view: MenuView
        self._button_group: ButtonGroup

    def run(self) -> None:
        self._menu_view = MenuView(self)
        self._window.show_view(self._menu_view)

        arcade.run()

    def start(self) -> None:
        # 1 - create levels
        # 2 - start the first level
        maze_width = 7
        maze_height = 7
        cell_size = 72

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

        blinky = Ghost("assets/blinky.png", 12, 4.5, maze, player)
        b_position = maze.get_cell(0, 0)
        blinky.setup(b_position)
        level = Level(player, maze, [blinky], self._game_config.level_max_time, self._menu_view)

        self._window.show_view(level)

    def pause(self) -> None:
        pass

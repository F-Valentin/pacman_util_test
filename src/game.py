import arcade
from level import Level
from entity.player import Player
from maze import Maze
from typing import TYPE_CHECKING
from views import MenuView

if TYPE_CHECKING:
    from game_configuration import GameConfig


class Game:
    def __init__(self, window: arcade.Window, game_config: GameConfig) -> None:
        self.__window = window
        self.__game_config = game_config
        self.__menu_view: arcade.View
    

    def run(self) -> None:
        self.__menu_view = MenuView(self)
        self.__window.show_view(self.__menu_view)

        arcade.run()

    def start(self) -> None:
        # 1 - create levels
        # 2 - start the first level
        maze_width = 3
        maze_height = 3
        cell_size = 72

        offset_x: int = (
            (self.__game_config.screen_width -
             maze_width * cell_size) // 2
        )

        offset_y: int = (
            (self.__game_config.screen_height -
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

        maze.setup(self.__game_config.points_per_pacgum)
        player = Player(maze)

        half = maze_width * cell_size // 2
        offset = 0 if maze_width % 2 != 0 else -cell_size // 2
        x = int(offset_x + half + offset)
        y = int(offset_y  + half + offset)

        score_ui_y = offset_y + maze_height * cell_size + 100


        p_position = arcade.Vec2(x, y)
        score_ui_pos = arcade.Vec2(offset_x, score_ui_y)

        player.setup(p_position, score_ui_pos)
        level = Level(player, maze)

        self.__window.show_view(level)

    def pause(self) -> None:
        pass

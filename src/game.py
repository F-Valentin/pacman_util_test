import arcade
from level import Level
from entity.player import Player
from maze import Maze
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_configuration import GameConfig


class Game:
    def __init__(self, window: arcade.Window, game_config: GameConfig) -> None:
        self.__window = window
        self.__game_config = game_config

    def start(self) -> None:
        # 1 - create levels
        # 2 - start the first level
        maze_width = 10
        maze_height = 10
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

        maze.setup()
        player = Player(maze)
        half = maze_width * cell_size // 2
        offset = 0 if maze_width % 2 != 0 else -cell_size // 2
        x = int(offset_x + half + offset)
        y = int(offset_y  + half + offset)


        print((x, y))
        player.position = (x, y)
        player.setup()
        level = Level(player, maze)
        self.__window.show_view(level)

    def pause(self) -> None:
        pass

import arcade
from game_configuration import GameConfig
from level import LevelFactory, LevelManager
from player import Player
from cell import Cell
from mazegenerator import MazeGenerator
from game_setting import GameSettings
from algorithm_strategy import DFSStrategy


def main():

    game_settings = GameSettings()
    window = arcade.Window(
        width=game_settings.screen_width,
        height=game_settings.screen_height)
    level_manager = LevelManager(window)
    game_config = GameConfig("../config.json")
    player = Player()
    level_factory = LevelFactory(
        player=player,
        game_config=game_config,
        ghost_strategy=DFSStrategy(),
        maze_size=(
            15,
            10),
        level_switcher=level_manager,
        game_settings=game_settings)
    level1 = level_factory.create_level()
    level1._setup_cells()
    window.show_view(level1)
    arcade.run()
    # set the position of the player with set_position
    # player.set_position()


if __name__ == "__main__":
    main()

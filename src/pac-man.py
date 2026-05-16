import arcade
from game_configuration import GameConfig
from level import LevelFactory, LevelManager
from player import Player
from algorithm_strategy import DFSStrategy
from view_manager import ViewManager


def main() -> None:

    game_config = GameConfig("config.json")
    window = arcade.Window(
        width=game_config.screen_width,
        height=game_config.screen_height)
    view_manager = ViewManager(window)
    level_manager = LevelManager(window)
    player = Player()
    level_factory = LevelFactory(
        player=player,
        game_config=game_config,
        ghost_strategy=DFSStrategy(),
        maze_size=(15, 15),
        level_switcher=level_manager)
    level1 = level_factory.create_level()
    window.show_view(level1)
    arcade.run()


if __name__ == "__main__":
    main()

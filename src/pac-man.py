import arcade
from game.game_configuration import GameConfig
from level.level import LevelFactory, LevelManager
from player.player import Player
from algorithms.algorithm_strategy import DFSStrategy
from view_manager import ViewManager
from game.game_state import GameState


def main() -> None:

    game_config = GameConfig("config.json")
    window = arcade.Window(
        width=game_config.screen_width,
        height=game_config.screen_height)
    view_manager = ViewManager(window)
    game_state = GameState(view_manager)
    level_manager = LevelManager(window)
    player = Player()
    level_factory = LevelFactory(
        player=player,
        game_config=game_config,
        ghost_strategy=DFSStrategy(),
        maze_size=(15, 15),
        level_switcher=level_manager)
    player.add_death_subscriber(game_state)
    level_manager.add_subscriber(game_state)
    level1 = level_factory.create_level()
    level_manager.append_level(level1)
    window.show_view(level1)
    arcade.run()


if __name__ == "__main__":
    main()

import arcade
import sys
from game.game_configuration import GameConfig
from level.level import LevelFactory, LevelManager
from player.player import Player
from algorithms.algorithm_strategy import BFSStrategy
from view_manager import ViewManager
from game.game_state import GameState
from views import WinView


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        return

    file_path = sys.argv[1]

    game_config = GameConfig(file_path)
    window = arcade.Window(
        width=game_config.screen_width,
        height=game_config.screen_height)
    view_manager = ViewManager(window)
    view_manager.add_view("win_view", WinView())
    game_state = GameState(view_manager)
    level_manager = LevelManager(window)
    player = Player(game_config.lives)
    level_factory = LevelFactory(
        player=player,
        game_config=game_config,
        maze_size=(3, 3),
        level_switcher=level_manager)
    player.add_death_subscriber(game_state)
    level_manager.add_subscriber(game_state)
    level1 = level_factory.create_level()
    # level2 = level_factory.create_level()
    # level_manager.append_levels([level1, level2])
    level_manager.append_level(level1)
    window.show_view(level1)
    arcade.run()


if __name__ == "__main__":
    main()

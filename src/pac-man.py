import arcade
import sys
from game import Game
from game_configuration import GameConfig
from views import MenuView


def main() -> None:
    """ Main function """
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        return

    file_path = sys.argv[1]

    game_config = GameConfig(file_path)

    window = arcade.Window(game_config.screen_width, game_config.screen_height)
    game = Game(window, game_config)
    window.show_view(MenuView(game))

    arcade.run()


if __name__ == "__main__":
    main()

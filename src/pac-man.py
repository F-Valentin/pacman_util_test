import arcade
import sys
from game.game_configuration import GameConfig
from views import StartView


def main() -> None:

    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        return

    file_path = sys.argv[1]

    game_config = GameConfig(file_path)
    window = arcade.Window(
        width=game_config.screen_width,
        height=game_config.screen_height)
    start_view = StartView(window, game_config)
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()

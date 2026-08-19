import sys

import arcade

from game import Game
from game_configuration import GameConfig


def main() -> None:
    """Launch the Pac-Man game using the provided configuration file."""
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>")
        return

    file_path = sys.argv[1]

    try:
        game_config = GameConfig(file_path)
    except (FileNotFoundError, ValueError, PermissionError) as e:
        print(f"[Config Error] {e}")
        return

    window = arcade.Window(game_config.screen_width,
                           game_config.screen_height)
    game = Game(window, game_config)
    game.run()


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as e:
        print(e)
    except KeyboardInterrupt:
        pass

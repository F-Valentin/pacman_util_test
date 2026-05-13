from dataclasses import dataclass


@dataclass
class GameSettings:
    tile_size: int = 50
    screen_width: int = 800
    screen_height: int = 800
    movement_speed: float = 2.5
    maze_size: int = 15

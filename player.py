import arcade
from typing import Optional
from game_seting import GameSettings


class Player:
    def __init__(self, start_x: float, start_y: float, settings: GameSettings
                 ) -> None:

        self.settings = settings
        self.sprite = arcade.load_animated_gif("pacman.gif")
        self.sprite.scale = 0.09
        self.sprite.center_x = start_x
        self.sprite.center_y = start_y

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self._sprite_list = arcade.SpriteList()
        self._sprite_list.append(self.sprite)

        self.direction: Optional[str] = None
        self.next_direction: Optional[str] = None

    def update(self, dt: float) -> None:
        self._sprite_list.update_animation(dt)
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def draw(self) -> None:
        self._sprite_list.draw()

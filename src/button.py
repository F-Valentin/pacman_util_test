import arcade
from arcade.types import PathOrTexture
from utils import Rect
from collections.abc import Callable
from enum import Enum

class ButtonType(Enum):
    START = 0
    EXIT = 0

class Button:
    def __init__(self, name: str, x: float, y: float,
                 path_to_images: str, callable: Callable) -> None:
        self._name = name
        self.center: arcade.Vec2 = arcade.Vec2(x, y)
        self._sprite: arcade.Sprite = arcade.Sprite(path_to_images)
        self._sprite_list = arcade.SpriteList()
        self.trigger = callable

        top_left_x = x - self._sprite.width // 2
        top_left_y = y + self._sprite.height // 2

        self.collision_rect: Rect = Rect(
            top_left_x,
            top_left_y,
            self._sprite.width,
            self._sprite.height)

        self._sprite.position = self.center
        self._sprite_list.append(self._sprite)
    
    @property
    def name(self) -> str:
        return self._name

    def set_alpha(self, value: int) -> None:
        self._sprite.alpha = value

    def draw(self) -> None:
        self._sprite_list.draw()
        # arcade.draw_circle_filled(self.center.x, self.center.y, 6, arcade.color.WHITE)
    
    def collide_with_point(self, point: arcade.Vec2) -> bool:
        rect = self.collision_rect

        if (
            point.x < rect.x or point.x > rect.x + rect.width
            or point.y > rect.y or point.y < rect.y - rect.height
        ):
            return False

        return True


import arcade
from arcade.types import PathOrTexture
from utils import Rect
from collections.abc import Callable


class Button:
    def __init__(self, name: str, x: float, y: float,
                 path_to_images: str, callable: Callable) -> None:
        self._name = name
        self.center: arcade.Vec2 = arcade.Vec2(x, y)
        self.__sprite: arcade.Sprite = arcade.Sprite(path_to_images)
        self.__sprite_list = arcade.SpriteList()
        self.trigger = callable

        top_left_x = x - self.__sprite.width // 2
        top_left_y = y + self.__sprite.height // 2

        self.collision_rect: Rect = Rect(
            top_left_x,
            top_left_y,
            self.__sprite.width,
            self.__sprite.height)

        self.__sprite.position = self.center
        self.__sprite_list.append(self.__sprite)

    def set_alpha(self, value: int) -> None:
        self.__sprite.alpha = value

    def draw(self) -> None:
        self.__sprite_list.draw()
        # arcade.draw_circle_filled(self.center.x, self.center.y, 6, arcade.color.WHITE)

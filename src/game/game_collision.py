import arcade
import math


def check_collision(sprite_a: arcade.Sprite,
                    sprite_b: arcade.Sprite) -> bool:
    dx = sprite_a.center_x - sprite_b.center_x
    dy = sprite_a.center_y - sprite_b.center_y
    distance = math.sqrt(dx**2 + dy**2)

    radius_a = (sprite_a.width / 2) * 0.5
    radius_b = (sprite_b.width / 2) * 0.5

    return distance < (radius_a + radius_b)

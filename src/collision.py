import arcade
from utils import Rect


def is_point_in_rect(point: arcade.Vec2, rect: Rect) -> bool:
    if (
        point.x < rect.x or point.x > rect.x + rect.width
        or point.y > rect.y or point.y < rect.y - rect.height
    ):
        return False

    return True

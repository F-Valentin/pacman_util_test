import arcade


class HitBox:
    """
        Hit-test rectangle. x/y = top-left corner
        (arcade coords: y increases upward).
    """

    def __init__(self, x: float, y: float,
                 width: float,
                 height: float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def collide_with_point(self, point: arcade.Vec2) -> bool:
        rect = self

        return not (
            point.x < rect.x or point.x > rect.x + rect.width
            or point.y > rect.y or point.y < rect.y - rect.height
        )

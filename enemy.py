import arcade

from arcade.types import PathOrTexture

from algorithm_strategy import PathfindingStrategy


class Ghost(arcade.Sprite):
    def __init__(self, path_to_animation: str,
                 strategy: PathfindingStrategy) -> None:
        super().__init__()
        self._sprite_list: arcade.SpriteList = arcade.SpriteList()
        self._animation = arcade.load_animated_gif(path_to_animation)
        self._sprite_list.append(self._animation)
        # self.speed
        self._strategy = strategy

    @property
    def strategy(self) -> PathfindingStrategy:
        return self._strategy

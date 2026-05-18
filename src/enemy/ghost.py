import arcade
from arcade import SpriteList
from subscriber import IGhostSubscriber
from algorithms.algorithm_strategy import PathfindingStrategy


class Ghost():

    def __init__(self, path_to_sprite: str,
                 algo: PathfindingStrategy) -> None:
        self.sprite: arcade.Sprite = arcade.Sprite(path_to_sprite)
        self.sprite.scale = 0.06

        self._sprite_list: SpriteList[arcade.Sprite] = SpriteList()
        self._sprite_list.append(self.sprite)

        self._subscribers: list[IGhostSubscriber] = []

        self.algo = algo

    def set_position(self, x: int, y: int) -> None:
        self.sprite.center_x = x
        self.sprite.center_y = y

    def update(self) -> None:
        self._sprite_list.update()

    def draw(self) -> None:
        self._sprite_list.draw()

    @property
    def subscribers(self) -> list[IGhostSubscriber]:
        return self._subscribers

    def add_subscriber(self, subscriber: IGhostSubscriber) -> None:
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: IGhostSubscriber) -> None:
        self._subscribers.remove(subscriber)

    def die(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_ghost_death()

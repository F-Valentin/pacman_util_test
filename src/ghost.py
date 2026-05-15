import arcade
from algorithm_strategy import PathfindingStrategy
from subsriber import IGhostSubscriber, IPlayerSubscriber


class Ghost(arcade.Sprite):
    def __init__(self, path_to_animation: str,
                 strategy: PathfindingStrategy) -> None:
        super().__init__()

        self._sprite_list: arcade.SpriteList = arcade.SpriteList()
        self._animation = arcade.load_animated_gif(path_to_animation)
        self._sprite_list.append(self._animation)

        self._strategy = strategy

        self._subscribers: list[IGhostSubscriber] = []

    @property
    def strategy(self) -> PathfindingStrategy:
        return self._strategy

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

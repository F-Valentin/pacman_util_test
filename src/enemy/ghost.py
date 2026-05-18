import arcade
from arcade import SpriteList
from maze.cell import Cell
from subscriber import IGhostSubscriber
from algorithms.algorithm_strategy import PathfindingStrategy


class Ghost():

    def __init__(self, path_to_sprite: str,
                 algo: PathfindingStrategy) -> None:
        self.sprite: arcade.Sprite = arcade.Sprite(path_to_sprite)
        self.sprite.scale = 0.06
        self.sprite.center_x = 0
        self.sprite.center_y = 0
        self.speed: float = 1.75

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self.actual_cell: Cell = None

        self._sprite_list: SpriteList[arcade.Sprite] = SpriteList()
        self._sprite_list.append(self.sprite)

        self._subscribers: list[IGhostSubscriber] = []

        self.algo = algo

    def set_position(self, x: int, y: int, cell: Cell) -> None:
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.actual_cell = cell

    def update(self, dt: float) -> None:
        self._sprite_list.update(dt)
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def draw(self) -> None:
        self._sprite_list.draw()

    def move_to_next_cell(self, cell: Cell) -> None:
        speed: float = self.speed

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

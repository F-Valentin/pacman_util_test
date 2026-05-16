from subscriber import IPacgumSubscriber
from pacgum import Pacgum


class Cell:
    """Cellule class used to create better coordinate system."""

    def __init__(self, x: int, y: int, walls: int, size: tuple[int, int],
                 has_visited: bool):
        self.x: int = x
        self.y: int = y
        self.size: tuple[int, int] = size
        self.walls: int = walls
        self.has_visited: bool = has_visited
        self.neighbors: list[tuple[int, int]] = [
            (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        self.center: tuple[int, int]
        self.has_pacgum: bool = True
        self.pacgum = Pacgum("normal", 10)
        self._subscribers: list[IPacgumSubscriber] = []

    def add_subscriber(self, subscriber: IPacgumSubscriber) -> None:
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: IPacgumSubscriber) -> None:
        self._subscribers.remove(subscriber)

    def pacgum_eaten(self) -> None:
        self.has_pacgum = False
        # notify level to change score

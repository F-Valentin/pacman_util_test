import arcade
from enum import Enum


class GhostState(str, Enum):
    IDLE = "idle"
    MOVE = "move"
    DEAD = "dead"


class Ghost(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.state: GhostState = GhostState.IDLE
        self.animations: dict[str, arcade.SpriteList] = {}

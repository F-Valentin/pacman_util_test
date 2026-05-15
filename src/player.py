from subsriber import IPlayerSubscriber

import arcade
from typing import Optional
# from game_seting import GameSettings
from cell import Cell


class Player:
    def __init__(self) -> None:
        # self.settings = settings
        self.sprite: arcade.TextureAnimationSprite = arcade.load_animated_gif(
            "../assets/pacman.gif")
        self.sprite.scale = 0.09
        self.sprite.center_x = 0
        self.sprite.center_y = 0

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self._sprite_list: arcade.SpriteList[arcade.TextureAnimationSprite] = arcade.SpriteList(
        )
        self._sprite_list.append(self.sprite)

        self.speed: float = 2.5
        self.direction: Optional[str] = None
        self.next_direction: Optional[str] = None
        self._subscribers: list[IPlayerSubscriber] = []

    @property
    def subscribers(self) -> list[IPlayerSubscriber]:
        return self._subscribers

    def update(self, dt: float) -> None:
        self._sprite_list.update_animation(dt)
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def set_position(self, x: int, y: int):
        self.sprite.center_x = x
        self.sprite.center_y = y

    def move_to_next_cell(self, cell: Cell) -> None:
        self.change_x = 0.0
        self.change_y = 0.0
        next_dir = self.next_direction
        speed: float = self.speed

        if next_dir == "UP" and not cell.walls & 0b0001:
            self.sprite.angle = -90
            self.next_direction = None
            self.direction = "UP"
            self.change_y = speed
        elif next_dir == "DOWN" and not cell.walls & 0b0100:
            self.sprite.angle = 90
            self.next_direction = None
            self.direction = "DOWN"
            self.change_y = -speed
        elif next_dir == "RIGHT" and not cell.walls & 0b0010:
            self.sprite.angle = 0
            self.next_direction = None
            self.direction = "RIGHT"
            self.change_x = speed
        elif next_dir == "LEFT" and not cell.walls & 0b1000:
            self.sprite.angle = 180
            self.next_direction = None
            self.direction = "LEFT"
            self.change_x = -speed
        else:
            self.next_direction = self.direction

    def add_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.remove(subscriber)

    def die(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_death()

    def eat_super_pacgum(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_ate_super_pacgum()

    def level_completed(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_completed_level()

    def draw(self) -> None:
        self._sprite_list.draw()

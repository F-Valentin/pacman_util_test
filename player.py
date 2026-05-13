from subsriber import IPlayerSubscriber

import arcade
from typing import Optional
from game_seting import GameSettings


class Player:
    def __init__(self) -> None:
        self._subscribers: list[IPlayerSubscriber] = []

    @property
    def subscribers(self) -> list[IPlayerSubscriber]:
        return self._subscribers

    def add_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.append(subscriber)

    def remove_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.remove(subscriber)

    def die(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_death()

    def eat_pacgum(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_ate_super_pacgum()

    def level_completed(self) -> None:
        for subscriber in self._subscribers:
            subscriber.on_player_completed_level()


player = Player()

player.die()
player.level_completed()


class PACMANPlayer:
    def __init__(self, start_x: float, start_y: float, settings: GameSettings
                 ) -> None:

        self.settings = settings
        self.sprite = arcade.load_animated_gif("pacman.gif")
        self.sprite.scale = 0.09
        self.sprite.center_x = start_x
        self.sprite.center_y = start_y

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self._sprite_list = arcade.SpriteList()
        self._sprite_list.append(self.sprite)

        self.direction: Optional[str] = None
        self.next_direction: Optional[str] = None

    def update(self, dt: float) -> None:
        self._sprite_list.update_animation(dt)
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def draw(self) -> None:
        self._sprite_list.draw()

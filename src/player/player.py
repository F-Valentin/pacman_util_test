from maze.maze import Maze
from subscriber import IPlayerDeathSubscriber, IPlayerSubscriber


import arcade
from typing import Optional
from maze.cell import Cell
from arcade import SpriteList, TextureAnimationSprite


class Player:
    def __init__(self, lives: int) -> None:
        self.sprite: TextureAnimationSprite = arcade.load_animated_gif(
            "assets/pacman.gif")
        self.sprite.scale = 0.16
        self.sprite.center_x = 0
        self.sprite.center_y = 0

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self.actual_cell: Cell = None

        self._sprite_list: SpriteList[TextureAnimationSprite] = SpriteList()
        self._sprite_list.append(self.sprite)

        self.speed: float = 4.5
        self.lives = lives
        self.direction: Optional[str] = None
        self.next_direction: Optional[str] = None
        self._subscribers: list[IPlayerSubscriber] = []
        self._on_death_subsribers: list[IPlayerDeathSubscriber] = []

    def update(self, dt: float) -> None:
        self._sprite_list.update_animation(dt)
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def set_position(self, x: int, y: int, cell: Cell) -> None:
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.actual_cell = cell

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

        if cell.has_pacgum:
            cell.pacgum_eaten()

    def restart(self, maze: Maze) -> None:
        tile_size = maze.tile_size
        half = maze.width * tile_size // 2
        offset = 0 if maze.width % 2 != 0 else -tile_size // 2
        x: int = int(maze.offset_x + half + offset)
        y: int = int(maze.offset_y + half + offset)
        self.change_x = 0
        self.change_y = 0
        self.direction = None
        self.next_direction = None

        x_idx = int((x - maze.offset_x) / maze.tile_size)
        y_idx = int((y - maze.offset_y) / maze.tile_size)
        cell = maze.grid[y_idx][x_idx]
        self.set_position(x, y, cell)

    def add_player_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.append(subscriber)

    def add_death_subscriber(self, subscriber: IPlayerDeathSubscriber) -> None:
        self._on_death_subsribers.append(subscriber)

    def remove_player_subscriber(self, subscriber: IPlayerSubscriber) -> None:
        self._subscribers.remove(subscriber)

    def remove_death_subscriber(
            self, subscriber: IPlayerDeathSubscriber) -> None:
        self._on_death_subsribers.remove(subscriber)

    # TODO
    # def collide_with_enemies(self, )

    def die(self) -> None:
        print("die")
        for subscriber in self._on_death_subsribers:
            subscriber.on_player_death()

    def draw(self) -> None:
        self._sprite_list.draw()

    # def level_completed(self) -> None:
    #     for subscriber in self._subscribers:
    #         subscriber.on_player_completed_level()

import arcade
import math
from enum import Enum
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entity.ghost import Ghost
    from maze import Maze
    from cell import Cell


class PlayerState(str, Enum):
    IDLE = "idle"
    MOVE = "move"
    DEAD = "dead"


class PlayerDirection(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Player(arcade.Sprite):
    def __init__(self, maze: Maze) -> None:
        super().__init__()

        self._lives: int = 0
        self.next_direction: Optional[PlayerDirection] = None
        self.speed: float = 0.0
        self.state: PlayerState = PlayerState.MOVE
        self.animations: dict[str, arcade.SpriteList] = {}
        self._grid_coordinate: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.direction: Optional[PlayerDirection] = None
        self.__maze = maze

    def setup(self) -> None:
        move_animation = arcade.load_animated_gif("assets/pacman.gif")
        move_animation.position = self.position
        move_animation.scale = 0.1

        move_sprite_list = arcade.SpriteList()
        move_sprite_list.append(move_animation)
        self.speed = 4.5 
        self.__update_grid_coordinate()
        # print(len(move_sprite_list))

        self.animations["move"] = move_sprite_list
     

    def set_next_direction(self, key: int) -> None:
        match key:
            case arcade.key.UP | arcade.key.W:
                self.next_direction = PlayerDirection.UP
            case arcade.key.DOWN | arcade.key.S:
                self.next_direction = PlayerDirection.DOWN
            case arcade.key.LEFT | arcade.key.A:
                self.next_direction = PlayerDirection.LEFT
            case arcade.key.RIGHT | arcade.key.D:
                self.next_direction = PlayerDirection.RIGHT


    def get_grid_coordinate(self) -> arcade.Vec2:
        return self._grid_coordinate
    
    def get_current_cell(self) -> Cell:
        c_x = int(self._grid_coordinate.x)
        c_y = int(self._grid_coordinate.y)
        p_cell: Cell = self.__maze.get_cell(c_x, c_y)

        return p_cell

 
    def __update_grid_coordinate(self) -> None:
        cell_size: int = self.__maze.cell_size
        bottom_left_pos = self.__maze.bottom_left_pos

        x: float = (self.center_x - bottom_left_pos.x) / float(cell_size)
        y: float = ((self.__maze.height - 1) - (self.center_y - bottom_left_pos.y)) / float(cell_size)

        self._grid_coordinate = arcade.Vec2(
            math.floor(x),
            math.floor(y)
        )
    
    def __move(self, delta_time: float) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.__update_grid_coordinate()

        current_animation = self.animations[self.state]
        current_animation.update_animation(delta_time)
        current_animation[0].center_x = self.center_x
        current_animation[0].center_y = self.center_y

    
    def update(self, delta_time: float = 1/60, *args, **kwargs) -> None:
        self.__move(delta_time)

        cell = self.get_current_cell()
        if cell.center:
            px, py = int(self.center_x), int(self.center_y)
            cx, cy = int(cell.center.x), int(cell.center.y)
            if (px, py) == (cx, cy):
                self.move_to_next_cell(cell)

    
    def move_to_next_cell(self, p_cell: Cell) -> None:
        north, east, south, west = 0b0001, 0b0010, 0b0100, 0b1000
        sprite: arcade.TextureAnimationSprite = self.animations[self.state][0]
        speed = self.speed

        next_direction: Optional[PlayerDirection] = self.next_direction or self.direction

        self.change_x = 0.0
        self.change_y = 0.0

        if next_direction == PlayerDirection.UP and not p_cell.walls & north:
            sprite.angle = -90
            self.change_y = speed
            self.direction = next_direction
            self.next_direction = None
        elif next_direction == PlayerDirection.DOWN and not p_cell.walls & south:
            sprite.angle = 90
            self.change_y = -speed
            self.direction = next_direction
            self.next_direction = None
        elif next_direction == PlayerDirection.RIGHT and not p_cell.walls & east:
            sprite.angle = 0
            self.change_x = speed
            self.direction = next_direction
            self.next_direction = None
        elif next_direction == PlayerDirection.LEFT and not p_cell.walls & west:
            sprite.angle = 180
            self.change_x = -speed
            self.direction = next_direction
            self.next_direction = None
        else:
            self.next_direction = self.direction

    def collide_with_ghosts(self, ghosts: list[Ghost]) -> bool:
        for ghost in ghosts:
            dx: float = self.center_x - ghost.center_x
            dy: float = self.center_y - ghost.center_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            p_current_sprite: arcade.Sprite = self.animations[self.state][0]
            g_current_sprite: arcade.Sprite = ghost.animations[ghost.state][0]

            p_radius = (p_current_sprite.width / 2) * 0.5
            g_radius = (g_current_sprite.width / 2) * 0.5

            if distance <= (p_radius + g_radius):
                return True

        return False

    def draw(self) -> None:
        self.animations[self.state].draw()

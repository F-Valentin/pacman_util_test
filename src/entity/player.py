"""Player entity and movement logic for the Pac-Man prototype."""

import arcade
import math
from enum import Enum
from typing import Optional
from maze import Maze
from cell import Cell
from entity.ghost import Ghost, GhostState


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
    """Represent the controlled player character on the maze grid."""

    def __init__(self, position: arcade.Vec2, score: int) -> None:
        super().__init__()

        self.center_x = position.x
        self.center_y = position.y
        
        self._current_lives: int = 3
        self._default_position: arcade.Vec2 = position
        self.next_direction: Optional[PlayerDirection] = None
        self.speed: float = 4.0
        self.state: PlayerState = PlayerState.MOVE
        self.animations: dict[str, arcade.SpriteList] = {}
        self._grid_coordinate: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.direction: Optional[PlayerDirection] = None
        self.score: int = score
        self.ghosts: list[Ghost]
        self._invicibility = False
        
        # self._update_grid_coordinate()
        self._init_animation()

    @property
    def current_lives(self) -> int:
        return self._current_lives

    def _init_animation(self) -> None:
        move_animation = arcade.load_animated_gif("assets/pacman.gif")
        move_animation.position = self.position
        move_animation.scale = 0.12

        move_sprite_list: arcade.SpriteList = arcade.SpriteList()
        move_sprite_list.append(move_animation)

        self.animations["move"] = move_sprite_list

    def restart_position(self) -> None:
        """Reset the player to its starting cell after a collision."""
        self.center_x = self._default_position.x
        self.center_y = self._default_position.y
        self.velocity = 0.0, 0.0
        self.direction = None
        self.next_direction = None

    def set_next_direction(self, key: int) -> None:
        """Store the next direction chosen by the player from keyboard input."""
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

    def get_current_cell(self, maze: Maze) -> Cell:
        c_x = int(self._grid_coordinate.x)
        c_y = int(self._grid_coordinate.y)
        p_cell: Cell = maze.get_cell(c_x, c_y)

        return p_cell


    def _move(self, delta_time: float) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y

        current_animation = self.animations[self.state]
        current_animation.update_animation(delta_time)
        current_animation[0].center_x = self.center_x
        current_animation[0].center_y = self.center_y

    def _eat_pacgum(self, cell: Cell, maze: Maze) -> None:
        if cell.pacgum and cell.has_pacgum():
            cell.hide_pacgum()
            self._update_score(cell.pacgum.point)
            maze.pacgum_eaten()
            
            if cell.pacgum.is_super:
                for ghost in self.ghosts:
                    ghost.state = GhostState.FLEE

    def take_damage(self) -> None:
        if not self._invicibility:
            self._current_lives -= 1

    def update(self, maze: Maze, delta_time: float = 1 / 60) -> None:
        self._move(delta_time)
        self._grid_coordinate = maze.convert_pos_to_grid(arcade.Vec2(self.center_x, self.center_y))

        cell = self.get_current_cell(maze)
        if cell.center:
            px, py = int(self.center_x), int(self.center_y)
            cx, cy = int(cell.center.x), int(cell.center.y)
            if (px, py) == (cx, cy):
                self._eat_pacgum(cell, maze)
                self.move_to_next_cell(cell)

    def _update_score(self, value: int) -> None:
        self.score += value

    def move_to_next_cell(self, p_cell: Cell) -> None:
        """Move the player toward the next open adjacent maze cell."""
        north, east, south, west = 0b0001, 0b0010, 0b0100, 0b1000
        sprite: arcade.TextureAnimationSprite = self.animations[self.state][0]
        speed = self.speed

        next_direction: Optional[PlayerDirection] = (
            self.next_direction or self.direction)

        self.change_x = 0.0
        self.change_y = 0.0

        if next_direction == PlayerDirection.UP and not p_cell.walls & north:
            sprite.angle = -90
            self.change_y = speed
            self.direction = next_direction
            self.next_direction = None
        elif (next_direction == PlayerDirection.DOWN
              and not p_cell.walls & south):
            sprite.angle = 90
            self.change_y = -speed
            self.direction = next_direction
            self.next_direction = None
        elif (next_direction == PlayerDirection.RIGHT
              and not p_cell.walls & east):
            sprite.angle = 0
            self.change_x = speed
            self.direction = next_direction
            self.next_direction = None
        elif (next_direction == PlayerDirection.LEFT
              and not p_cell.walls & west):
            sprite.angle = 180
            self.change_x = -speed
            self.direction = next_direction
            self.next_direction = None
        else:
            self.next_direction = self.direction

    def collide_with_ghosts(self) -> bool:
        """Return whether the player overlaps any ghost sprite."""
        for ghost in self.ghosts:
            dx: float = self.center_x - ghost.center_x
            dy: float = self.center_y - ghost.center_y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            p_current_sprite: arcade.Sprite = self.animations[self.state][0]
            g_current_sprite: arcade.Sprite = ghost.animations[ghost.state][0]

            p_radius = (p_current_sprite.width / 2) * 0.5
            g_radius = (g_current_sprite.width / 2) * 0.5

            if (distance <= (p_radius + g_radius)
                    and ghost.state == GhostState.FLEE):
                ghost.restart_position()
                ghost.state = GhostState.MOVE
                return False
            elif distance <= (p_radius + g_radius):
                return True

        return False

    def invicibility(self) -> None:
        self._invicibility = not self._invicibility

    def draw(self) -> None:
        self.animations[self.state].draw()

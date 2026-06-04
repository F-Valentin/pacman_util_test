"""Player entity and movement logic for the Pac-Man prototype."""

import arcade
import math
from enum import Enum
from typing import TYPE_CHECKING, Optional
from maze import Maze
from score import ScoreUi
from cell import Cell
from entity.ghost import Ghost


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

    def __init__(self, maze: Maze) -> None:
        super().__init__()

        self._current_lives: int = 0
        self.lives: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()
        self._default_position: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.next_direction: Optional[PlayerDirection] = None
        self.speed: float = 0.0
        self.state: PlayerState = PlayerState.MOVE
        self.animations: dict[str, arcade.SpriteList] = {}
        self._grid_coordinate: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.direction: Optional[PlayerDirection] = None
        self.score: int = 0
        self._maze = maze
        self.score_ui: ScoreUi
    
    @property
    def current_lives(self) -> int:
        return self._current_lives

    def setup(self, position: arcade.Vec2, score_ui_pos: arcade.Vec2, hp_bar_pos: arcade.Vec2, lives: int) -> None:
        """Initialize the player sprite, score UI, and life indicators."""
        self.center_x = position.x
        self.center_y = position.y
        self.score_ui = ScoreUi(score_ui_pos, arcade.Text(f"score: {self.score}", score_ui_pos.x, score_ui_pos.y))
        self._current_lives = lives

        h_offset = 0
        for _ in range(lives):
            self.lives.append(
                arcade.Sprite("assets/hp.png", 1, hp_bar_pos.x + h_offset, hp_bar_pos.y)
            )
            h_offset += 40


        move_animation = arcade.load_animated_gif("assets/pacman.gif")
        move_animation.position = self.position
        move_animation.scale = 0.1

        move_sprite_list = arcade.SpriteList()
        move_sprite_list.append(move_animation)
        self.speed = 4.5 
        self._default_position = position
        self._update_grid_coordinate()

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
    
    def get_current_cell(self) -> Cell:
        c_x = int(self._grid_coordinate.x)
        c_y = int(self._grid_coordinate.y)
        p_cell: Cell = self._maze.get_cell(c_x, c_y)

        return p_cell

 
    def _update_grid_coordinate(self) -> None:
        cell_size: int = self._maze.cell_size
        bottom_left_pos = self._maze.bottom_left_pos

        x: float = (self.center_x - bottom_left_pos.x) / float(cell_size)
        y: float = ((self._maze.height - 1) - (self.center_y - bottom_left_pos.y)) / float(cell_size)

        self._grid_coordinate = arcade.Vec2(
            math.floor(x),
            math.floor(y)
        )
    
    def _move(self, delta_time: float) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
        self._update_grid_coordinate()

        current_animation = self.animations[self.state]
        current_animation.update_animation(delta_time)
        current_animation[0].center_x = self.center_x
        current_animation[0].center_y = self.center_y
    
    def _eat_pacgum(self, cell: Cell) -> None:
        if cell.pacgum and cell.has_pacgum():
            cell.hide_pacgum()
            self._update_score(cell.pacgum.point)
            self._maze.pacgum_eaten()
            self.update_score_ui()
    
    def take_damage(self) -> None:
        if self._current_lives:
            self._current_lives -= 1
    
    def update_score_ui(self) -> None:
        x = self.score_ui.position.x
        y = self.score_ui.position.y

        self.score_ui.score_text =  arcade.Text(f"score: {self.score}", x, y)

    def update(self, delta_time: float = 1/60, *args, **kwargs) -> None:
        self._move(delta_time)

        cell = self.get_current_cell()
        if cell.center:
            px, py = int(self.center_x), int(self.center_y)
            cx, cy = int(cell.center.x), int(cell.center.y)
            if (px, py) == (cx, cy):
                self._eat_pacgum(cell)
                self.move_to_next_cell(cell)
    
    def _update_score(self, value: int) -> None:
        self.score += value

    def move_to_next_cell(self, p_cell: Cell) -> None:
        """Move the player toward the next open adjacent maze cell."""
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
        """Return whether the player overlaps any ghost sprite."""
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
        self.score_ui.score_text.draw()

        for (i, live) in enumerate(self.lives):
            if i >= self._current_lives:
                live.alpha = 0
        
        self.lives.draw()

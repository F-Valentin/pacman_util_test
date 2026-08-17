"""Player entity and movement logic for the Pac-Man prototype."""

import math
from enum import Enum

import arcade

from cell import Cell, Walls
from entity.ghost import Ghost, GhostState
from maze import Maze
from paths import resource_path


class PlayerState(str, Enum):
    IDLE = "idle"
    MOVE = "move"
    DEAD = "dead"


class PlayerDirection(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


_DIRECTION_DELTA: dict[PlayerDirection, tuple[float, float]] = {
    PlayerDirection.UP: (0.0, 1.0),
    PlayerDirection.DOWN: (0.0, -1.0),
    PlayerDirection.LEFT: (-1.0, 0.0),
    PlayerDirection.RIGHT: (1.0, 0.0),
}

_DIRECTION_ANGLE: dict[PlayerDirection, float] = {
    PlayerDirection.UP: -90,
    PlayerDirection.DOWN: 90,
    PlayerDirection.LEFT: 180,
    PlayerDirection.RIGHT: 0,
}

_DIRECTION_WALL: dict[PlayerDirection, Walls] = {
    PlayerDirection.UP: Walls.NORTH,
    PlayerDirection.DOWN: Walls.SOUTH,
    PlayerDirection.LEFT: Walls.WEST,
    PlayerDirection.RIGHT: Walls.EAST,
}


class Player(arcade.Sprite):
    """Represent the controlled player character on the maze grid."""

    def __init__(self, position: arcade.Vec2, score: int,
                 maze: Maze, ghosts: list[Ghost],
                 lives: int = 3) -> None:
        super().__init__()

        self.center_x = position.x
        self.center_y = position.y

        self._current_lives: int = lives
        self._default_position: arcade.Vec2 = position
        self.next_direction: PlayerDirection | None = None
        self.speed: float = 4.0
        self.state: PlayerState = PlayerState.MOVE
        self.animations: dict[
            str, arcade.SpriteList[arcade.TextureAnimationSprite]
        ] = {}
        self.direction: PlayerDirection | None = None
        self.score: int = score
        self.ghosts: list[Ghost] = ghosts
        self._invicibility = False
        self._maze = maze

        self._start_center: arcade.Vec2 = position
        self._target_center: arcade.Vec2 = position
        self._t: float = 1.0

        self._init_animation()

    @property
    def current_lives(self) -> int:
        return self._current_lives

    def _init_animation(self) -> None:
        move_animation = arcade.load_animated_gif(
            resource_path("assets/pacman.gif"))
        move_animation.position = self.position
        move_animation.scale = 0.08

        move_sprite_list: arcade.SpriteList[arcade.TextureAnimationSprite] = (
            arcade.SpriteList()
        )
        move_sprite_list.append(move_animation)

        self.animations["move"] = move_sprite_list

    def restart_position(self) -> None:
        """Reset the player to its starting cell after a collision."""
        self.center_x = self._default_position.x
        self.center_y = self._default_position.y
        self.velocity = 0.0, 0.0
        self._start_center = self._default_position
        self._target_center = self._default_position
        self._t = 1.0
        self.direction = None
        self.next_direction = None

    def set_next_direction(self, key: int) -> None:
        """
            Store the next direction chosen
            by the player from keyboard input.
        """
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
        return self._maze.convert_pos_to_grid(
            arcade.Vec2(self.center_x, self.center_y))

    def get_current_cell(self) -> Cell:
        return self._maze.convert_pos_to_cell(
            arcade.Vec2(self.center_x, self.center_y))

    def _set_facing(self, direction: PlayerDirection) -> None:
        self.direction = direction
        self.animations[self.state][0].angle = _DIRECTION_ANGLE[direction]

    def _advance_position(self) -> None:
        if self.next_direction and self._opposite_direction(
                self.next_direction):
            tmp = self._start_center
            self._start_center = self._target_center
            self._target_center = tmp
            self._t = 1.0 - self._t
            self._set_facing(self.next_direction)
            self.next_direction = None

        if self._t < 1.0:
            self._t += self.speed / self._maze.cell_size

        if self._t >= 1.0:
            overshoot = self._t - 1.0

            self.center_x, self.center_y = self._target_center

            cell = self._maze.convert_pos_to_cell(self._target_center)
            self._eat_pacgum(cell)

            if (self.move_to_next_cell(cell)):
                self._t = overshoot
        else:
            self.center_x, self.center_y = arcade.math.lerp_2d(
                self._start_center, self._target_center, self._t)

    def _move(self, delta_time: float) -> None:
        self._advance_position()

        current_animation = self.animations[self.state]
        current_animation.update_animation(delta_time)
        current_animation[0].center_x = self.center_x
        current_animation[0].center_y = self.center_y

    def _eat_pacgum(self, cell: Cell) -> None:
        if cell.pacgum and cell.has_pacgum():
            cell.hide_pacgum()
            self._update_score(cell.pacgum.point)
            self._maze.pacgum_eaten()

            if cell.pacgum.is_super:
                for ghost in self.ghosts:
                    ghost.state = GhostState.FLEE

    def take_damage(self) -> None:
        if not self._invicibility:
            self._current_lives -= 1

    def update(self, delta_time: float = 1 / 60) -> None:
        self._move(delta_time)

    def _update_score(self, value: int) -> None:
        self.score += value

    def _opposite_direction(self, direction: PlayerDirection) -> bool:
        opp: PlayerDirection

        match direction:
            case PlayerDirection.UP:
                opp = PlayerDirection.DOWN
            case PlayerDirection.DOWN:
                opp = PlayerDirection.UP
            case PlayerDirection.LEFT:
                opp = PlayerDirection.RIGHT
            case PlayerDirection.RIGHT:
                opp = PlayerDirection.LEFT

        return opp == self.direction

    def move_to_next_cell(self, p_cell: Cell) -> bool:
        candidate: PlayerDirection | None = (
            self.next_direction or self.direction)

        if candidate is None:
            return False

        if p_cell.walls & _DIRECTION_WALL[candidate]:
            self.next_direction = self.direction
            return False

        dx, dy = _DIRECTION_DELTA[candidate]
        sprite: arcade.TextureAnimationSprite = self.animations[self.state][0]
        sprite.angle = _DIRECTION_ANGLE[candidate]

        self._start_center = arcade.Vec2(self.center_x, self.center_y)
        self._target_center = arcade.Vec2(
            self._start_center.x + dx * self._maze.cell_size,
            self._start_center.y + dy * self._maze.cell_size,
        )

        self.direction = candidate
        self.next_direction = None
        return True

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
                self._update_score(ghost.point)
                return False
            elif distance <= (p_radius + g_radius):
                return True

        return False

    @property
    def invivibility(self) -> bool:
        return self._invicibility

    def toggle_invicibility(self) -> None:
        self._invicibility = not self._invicibility

    def draw(self) -> None:
        self.animations[self.state].draw()

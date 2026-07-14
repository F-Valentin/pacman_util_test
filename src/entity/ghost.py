from __future__ import annotations
import arcade
import math
from enum import Enum
from collections import deque
from typing import Deque, Optional

from cell import Cell
from maze import Maze

"""Ghost AI and movement helpers for the level."""

class GhostState(str, Enum):
    IDLE = "idle"
    MOVE = "move"
    DEAD = "dead"
    FLEE = "flee"


class Ghost(arcade.Sprite):
    """Represent an enemy ghost that pursues the player through the maze."""

    def __init__(self, path_to_sprite: str, difficulty_id: int,
                 speed: float, maze: Maze) -> None:
        super().__init__()
        self.state: GhostState = GhostState.MOVE
        self.animations: dict[str, arcade.SpriteList] = {}
        self._grid_coordinate: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.path: list[Cell] = []
        self.difficulty_id = difficulty_id
        self.speed = speed
        self._maze = maze
        self._default_position: arcade.Vec2
        self._sprite_image = path_to_sprite
        self._flee_image = "assets/ghost_flee.png"
        self._freeze = False

    def setup(self, cell_pos: Cell) -> None:
        """Place the ghost at the given maze cell and prepare its sprite."""
        if not cell_pos.center:
            return

        position = arcade.Vec2(cell_pos.center.x, cell_pos.center.y)
        move_animation = arcade.Sprite(self._sprite_image)
        move_animation.position = position
        move_animation.scale = 0.08

        flee_animation = arcade.Sprite(self._flee_image)
        flee_animation.position = position
        flee_animation.scale = 0.08

        self.center_x = position.x
        self.center_y = position.y
        self.velocity = 0.0, 0.0

        move_sprite_list: arcade.SpriteList = arcade.SpriteList()
        move_sprite_list.append(move_animation)

        flee_sprite_list: arcade.SpriteList = arcade.SpriteList()
        flee_sprite_list.append(flee_animation)

        self.animations["move"] = move_sprite_list
        self.animations["flee"] = flee_sprite_list

        self.center_x = position.x
        self.center_y = position.y
        self._default_position = position
        self._spawn_cell = cell_pos

        self._update_grid_coordinate()

    def get_grid_coordinate(self) -> arcade.Vec2:
        return self._grid_coordinate

    def get_current_cell(self) -> Cell:
        c_x = int(self._grid_coordinate.x)
        c_y = int(self._grid_coordinate.y)

        g_cell: Cell = self._maze.get_cell(c_x, c_y)
        return g_cell

    def _update_grid_coordinate(self) -> None:
        cell_size: int = self._maze.cell_size
        bottom_left_pos = self._maze.bottom_left_pos

        x: float = (self.center_x - bottom_left_pos.x) / float(cell_size)
        y: float = ((self._maze.height - 1)
                    - (self.center_y - bottom_left_pos.y)) / float(cell_size)

        self._grid_coordinate = arcade.Vec2(
            math.floor(x),
            math.floor(y)
        )

    def restart_position(self) -> None:
        """Reset the ghost to its starting cell after a collision."""
        self.center_x = self._default_position.x
        self.center_y = self._default_position.y
        self.velocity = 0.0, 0.0
        self.path = []
        self.state = GhostState.MOVE
        self.change_x = 0.0
        self.change_y = 0.0

    def _path_to_cell(self, target_cell: Cell) -> list[Cell]:
        """Compute a simple shortest path from the ghost to the player's cell."""
        start = self.get_current_cell()

        start_coord = (start.grid_x, start.grid_y)
        dest_coord = (target_cell.grid_x, target_cell.grid_y)

        queue: Deque[Cell] = deque([start])

        came_from: dict[tuple[float, float],
                        Optional[tuple[float, float]]] = {start_coord: None}

        cell_registry: dict[tuple[float, float], Cell] = {start_coord: start}

        while queue:
            curr_cell: Cell = queue.popleft()
            curr_coord = (curr_cell.grid_x, curr_cell.grid_y)

            if curr_coord == dest_coord:
                break

            neighbors = self._maze._get_valid_cell_neighbors(curr_cell)

            if not neighbors:
                continue

            for neighbor in neighbors:
                neighbor_coord = (neighbor.grid_x, neighbor.grid_y)

                if neighbor_coord not in came_from:
                    came_from[neighbor_coord] = curr_coord
                    cell_registry[neighbor_coord] = neighbor
                    queue.append(neighbor)

        path = []
        curr: Optional[tuple[float, float]] = dest_coord

        while curr:
            path.append(cell_registry[curr])
            curr = came_from[curr]

        path.reverse()

        return path

    def _set_velocity_towards(self, target_cell: Cell) -> None:
        """Helper to set velocity vectors toward an adjacent cell."""
        g_cell = self.get_current_cell()

        if target_cell.grid_x > g_cell.grid_x:
            self.change_x = self.speed
            self.change_y = 0.0
        elif target_cell.grid_x < g_cell.grid_x:
            self.change_x = -self.speed
            self.change_y = 0.0
        elif target_cell.grid_y > g_cell.grid_y:
            self.change_x = 0.0
            self.change_y = -self.speed
        elif target_cell.grid_y < g_cell.grid_y:
            self.change_x = 0.0
            self.change_y = self.speed

    def _move_to_the_player(self, p_cell: Cell) -> None:
        """Advance the ghost toward the next step along its path."""

        if not self.path:
            path_to_player = self._path_to_cell(p_cell)
            if path_to_player and len(path_to_player) > 1:
                limite = self.difficulty_id
                self.path = path_to_player[1: 1 + limite]
            else:
                return

        target_cell = self.path.pop(0)
        self._set_velocity_towards(target_cell)

    def flee(self) -> None:
        """Advance the ghost toward its original spawn point."""
        if not self.path:
            path_to_spawn = self._path_to_cell(self._spawn_cell)
            if path_to_spawn and len(path_to_spawn) > 1:
                self.path = path_to_spawn[1:]
            else:
                return

        target_cell = self.path.pop(0)
        self._set_velocity_towards(target_cell)

    def _sync_animations(self, delta_time: float) -> None:
        """Sync all animations to the ghost's current position."""
        for anim in self.animations.values():
            if len(anim) > 0:
                anim[0].center_x = self.center_x
                anim[0].center_y = self.center_y
                anim.update_animation(delta_time)

    def update(self, p_cell: Cell, delta_time: float = 1 / 60) -> None:
        """Move the ghost and recompute its path when it reaches a cell."""
        if self._freeze:
            self._sync_animations(delta_time)
            return

        self.center_x += self.change_x
        self.center_y += self.change_y
        self._update_grid_coordinate()

        self._sync_animations(delta_time)

        cell = self.get_current_cell()

        if cell.center:
            gx, gy = int(self.center_x), int(self.center_y)
            cx, cy = int(cell.center.x), int(cell.center.y)
            if (gx, gy) == (cx, cy) and self.state != GhostState.FLEE:
                self._move_to_the_player(p_cell)
            elif ((gx, gy) == (cx, cy)
                  and self.state == GhostState.FLEE
                  and cell.grid_x == self._spawn_cell.grid_x
                  and cell.grid_y == self._spawn_cell.grid_y):
                self.state = GhostState.MOVE
                self.change_x = 0.0
                self.change_y = 0.0
                self.path = []
            elif (gx, gy) == (cx, cy) and self.state == GhostState.FLEE:
                self.flee()

    def toggle_freeze(self) -> None:
        self._freeze = not self._freeze

    def draw(self) -> None:
        self.animations[self.state].draw()

from __future__ import annotations

from collections import deque
from enum import Enum

import arcade
from typing_extensions import Any

from cell import Cell
from maze import Maze
from paths import resource_path

"""Ghost AI and movement helpers for the level."""


class GhostState(str, Enum):
    IDLE = "idle"
    MOVE = "move"
    DEAD = "dead"
    FLEE = "flee"


class Ghost(arcade.Sprite):
    """Represent an enemy ghost that pursues the player through the maze."""

    def __init__(
        self,
        position: arcade.Vec2, point: int,
        path_to_sprite: str, difficulty_id: int,
        speed: float, maze: Maze, _internal: bool = False
    ) -> None:
        """Do not use the default constructor"""
        if not _internal:
            raise RuntimeError("Use Ghost.at_cell() instead")
        super().__init__()

        self.center_x = position.x
        self.center_y = position.y
        self.state: GhostState = GhostState.MOVE
        self.animations: dict[str, arcade.SpriteList[arcade.Sprite]] = {}
        self._grid_coordinate: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.path: list[Cell] = []
        self.difficulty_id = difficulty_id
        self.speed = speed
        self._default_position: arcade.Vec2 = position
        self._sprite_image = path_to_sprite
        self._flee_image = "assets/ghost_flee.png"
        self._freeze = False
        self._spawn_cell: Cell
        self._maze = maze
        self.point = point

        self._init_animation()

    @classmethod
    def at_cell(
        cls,
        cell: Cell, point: int,
        path_to_sprite: str, difficulty_id: int,
        speed: float, maze: Maze
    ) -> Ghost:

        position = arcade.Vec2(cell.center.x, cell.center.y)

        ghost = cls(
            position,
            point,
            path_to_sprite,
            difficulty_id,
            speed,
            maze,
            _internal=True)
        ghost._spawn_cell = cell

        return ghost

    def _init_animation(self) -> None:
        move_animation = arcade.Sprite(resource_path(self._sprite_image))
        move_animation.position = self.position
        move_animation.scale = 0.06

        flee_animation = arcade.Sprite(resource_path(self._flee_image))
        flee_animation.position = self.position
        flee_animation.scale = 0.06

        move_sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        move_sprite_list.append(move_animation)

        flee_sprite_list: arcade.SpriteList[arcade.Sprite] = (
            arcade.SpriteList()
        )
        flee_sprite_list.append(flee_animation)

        self.animations["move"] = move_sprite_list
        self.animations["flee"] = flee_sprite_list

    def get_grid_coordinate(self) -> arcade.Vec2:
        return self._grid_coordinate

    def get_current_cell(self) -> Cell:
        c_x = int(self._grid_coordinate.x)
        c_y = int(self._grid_coordinate.y)

        g_cell: Cell = self._maze.get_cell(c_x, c_y)
        return g_cell

    def restart_position(self) -> None:
        """Reset the ghost to its starting cell after a collision."""
        self.center_x = self._default_position.x
        self.center_y = self._default_position.y
        self.velocity = 0.0, 0.0
        self.path = []
        self.state = GhostState.MOVE
        self.change_x = 0.0
        self.change_y = 0.0

    def _path_to_cell(self, start: Cell, target_cell: Cell) -> list[Cell]:
        """
            Compute a simple shortest path
            from the ghost to the player's cell.
        """

        start_coord = (start.grid_x, start.grid_y)
        dest_coord = (target_cell.grid_x, target_cell.grid_y)

        queue: deque[Cell] = deque([start])

        came_from: dict[tuple[float, float],
                        tuple[float, float] | None] = {start_coord: None}

        cell_registry: dict[tuple[float, float], Cell] = {start_coord: start}

        while queue:
            curr_cell: Cell = queue.popleft()
            curr_coord = (curr_cell.grid_x, curr_cell.grid_y)

            if curr_coord == dest_coord:
                break

            neighbors = self._maze.get_valid_cell_neighbors(curr_cell)

            if not neighbors:
                continue

            for neighbor in neighbors:
                neighbor_coord = (neighbor.grid_x, neighbor.grid_y)

                if neighbor_coord not in came_from:
                    came_from[neighbor_coord] = curr_coord
                    cell_registry[neighbor_coord] = neighbor
                    queue.append(neighbor)

        path = []
        curr: tuple[float, float] | None = dest_coord

        while curr:
            path.append(cell_registry[curr])
            curr = came_from[curr]

        path.reverse()

        return path

    def _set_velocity_towards(self, g_cell: Cell, target_cell: Cell) -> None:
        """Helper to set velocity vectors toward an adjacent cell."""

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

    def _navigate_to(self, target: Cell, limit: int | None = None) -> None:
        if not self.path:
            path = self._path_to_cell(self.get_current_cell(), target)
            if not path or len(path) <= 1:
                return
            self.path = path[1:] if limit is None else path[1: 1 + limit]

        self._set_velocity_towards(self.get_current_cell(), self.path.pop(0))

    def _move_to_the_player(self, p_cell: Cell) -> None:
        self._navigate_to(p_cell, limit=self.difficulty_id)

    def flee(self) -> None:
        self._navigate_to(self._spawn_cell)

    def _sync_animations(self, delta_time: float) -> None:
        """Sync all animations to the ghost's current position."""
        for anim in self.animations.values():
            if len(anim) > 0:
                anim[0].center_x = self.center_x
                anim[0].center_y = self.center_y
                anim.update_animation(delta_time)

    def update(
        self,
        delta_time: float = 1 / 60,
        *args: Any, **kwargs: Any
    ) -> None:
        """Move the ghost and recompute its path when it reaches a cell."""
        p_cell: Cell | None = kwargs.get("p_cell")

        if not p_cell:
            return

        if self._freeze:
            self._sync_animations(delta_time)
            return

        self.center_x += self.change_x
        self.center_y += self.change_y

        pos = arcade.Vec2(self.center_x, self.center_y)

        self._grid_coordinate = self._maze.convert_pos_to_grid(pos)

        self._sync_animations(delta_time)

        cell = self._maze.convert_pos_to_cell(pos)

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

from __future__ import annotations
import arcade
import math
from enum import Enum
from collections import deque
from typing import Deque, TYPE_CHECKING

from cell import Cell
from maze import Maze

if TYPE_CHECKING:
    from entity.player import Player

class GhostState(str, Enum):
    IDLE = "idle"
    MOVE = "move"
    DEAD = "dead"


class Ghost(arcade.Sprite):
    def __init__(self, path_to_sprite: str, difficulty_id: int, speed: float, maze: Maze, player: Player) -> None:
        super().__init__()
        self.state: GhostState = GhostState.MOVE
        self.animations: dict[str, arcade.SpriteList] = {}
        self._grid_coordinate: arcade.Vec2 = arcade.Vec2(0.0, 0.0)
        self.path: list[Cell] = []
        self.difficulty_id = difficulty_id
        self.speed = speed
        self._maze = maze
        self._default_position: arcade.Vec2
        self._player = player
        self._sprite_image = path_to_sprite
    
    def setup(self, cell_pos: Cell) -> None:
        if not cell_pos.center:
            return 

        position = arcade.Vec2(cell_pos.center.x, cell_pos.center.y)
        move_animation = arcade.Sprite(self._sprite_image)
        move_animation.position = position
        move_animation.scale = 0.08

        self.center_x = position.x
        self.center_y = position.y
        self.velocity = 0.0, 0.0

        move_sprite_list = arcade.SpriteList()
        move_sprite_list.append(move_animation)

        self.animations["move"] = move_sprite_list

        self.center_x = position.x
        self.center_y = position.y
        self._default_position = position

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
        y: float = ((self._maze.height - 1) - (self.center_y - bottom_left_pos.y)) / float(cell_size)

        self._grid_coordinate = arcade.Vec2(
            math.floor(x),
            math.floor(y)
        )
    
    def _path_to_player(self, p_cell) -> list[Cell]:
        start = self.get_current_cell()

        start_coord = (start.grid_x, start.grid_y)
        dest_coord = (p_cell.grid_x, p_cell.grid_y)

        queue: Deque[Cell] = deque([start])

        came_from: dict[tuple[float, float], tuple[float, float] | None] = {start_coord: None}

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
        curr = dest_coord

        while curr:
            path.append(cell_registry[curr])
            curr = came_from[curr]
        
        path.reverse()

        return path
    
    def _move_to_the_player(self) -> None:
        p_cell = self._player.get_current_cell()

        if not self.path:
            path_to_player = self._path_to_player(p_cell)
            if path_to_player and len(path_to_player) > 1:
                limite = self.difficulty_id

                self.path = path_to_player[1: 1 + limite]
            else:
                return
        
        g_cell = self.get_current_cell()
        target_cell = self.path.pop(0)

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

        

    
    def update(self, delta_time: float) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y
        self._update_grid_coordinate()

        current_animation = self.animations[self.state]
        current_animation[0].center_x = self.center_x
        current_animation[0].center_y = self.center_y
        current_animation.update_animation(delta_time)

        cell = self.get_current_cell()
        
        if cell.center:
            gx, gy = int(self.center_x), int(self.center_y)
            cx, cy = int(cell.center.x), int(cell.center.y)
            if (gx, gy) == (cx, cy):
                self._move_to_the_player()


       
    
    def draw(self) -> None:
        self.animations[self.state].draw()
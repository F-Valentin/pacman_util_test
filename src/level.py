"""Gameplay view implementation for the active maze level."""

from __future__ import annotations

import arcade
from typing import TYPE_CHECKING

from entity.ghost import Ghost
from entity.player import Player
from maze import Maze
from cell import Cell
from views import PauseView
from score import ScoreUi

if TYPE_CHECKING:
    from game import Game


class Level(arcade.View):
    """Represent the main level view where the player interacts with the maze."""

    def __init__(self, player: Player, maze: Maze,
                 ghosts: list[Ghost], time_to_finish: int,
                 game: Game) -> None:
        super().__init__()

        self._player = player
        self._maze = maze
        self._time_accumulator: float = 0
        self._time_to_finish = float(time_to_finish)
        self._ghosts = ghosts
        self._game = game
        self.score_ui: ScoreUi
        self.player_lives_ui: arcade.SpriteList[arcade.Sprite] = arcade.SpriteList()

        # h_offset = 0
        # for _ in range(self._player.current_lives):
        #     self.player_lives_ui.append(
        #         arcade.Sprite("assets/hp.png", 1,
        #                     hp_bar_pos.x + h_offset, hp_bar_pos.y)
        #     )
        #     h_offset += 40

    def setup(self) -> None:
        first_cell_pos = self._maze.get_cell(0, 0)

        if first_cell_pos.center:
            x = self._player._default_position.x
            y = first_cell_pos.center.y + 100
            score_ui_pos = arcade.Vec2(x, y)
            text = arcade.Text("score: {0}", x, y)
            self.score_ui = ScoreUi(score_ui_pos, text)

    def update_score_ui(self) -> None:
        x = self.score_ui.position.x
        y = self.score_ui.position.y

        self.score_ui.score_text = arcade.Text(
            f"score: {self._player.score}", x, y)

    def on_update(self, delta_time: float) -> None:
        """Update the level state each frame."""
        self._fixed_update(delta_time)

    def _fixed_update(self, delta_time: float) -> None:
        self._time_accumulator += delta_time
        time_step: float = 1 / 60

        while self._time_accumulator >= time_step:
            if self._time_to_finish <= 0:
                self._game.game_over(self._player.score)
                return

            if not self._maze.has_pacgums():
                self._game.next_level(self._player.score)
                return

            if self._player.collide_with_ghosts():
                self._player.take_damage()

                if not self._player.current_lives + 1:
                    self._game.game_over(self._player.score)
                    return

                self.restart_entity_position()

            self._player.update(self._maze, time_step)

            x = self._player.center_x
            y = self._player.center_y
            p_cell: Cell = self._maze.convert_pos_to_cell(arcade.Vec2(x, y))
            
            for ghost in self._ghosts:
                ghost.update(p_cell)

            self._time_accumulator -= time_step
            self._time_to_finish -= time_step
            self.update_score_ui()

    def restart_entity_position(self) -> None:
        """Reset the entities to their starting position after a collision."""
        self._player.restart_position()

        for ghost in self._ghosts:
            ghost.restart_position()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._player.set_next_direction(key=symbol)

        if symbol == arcade.key.SPACE:
            self.window.show_view(PauseView(self, self._game.cheat_mode))
        elif symbol == arcade.key.N:
            if self._game.can_skip_levels:
                self._game.next_level(self._player.score)

    def on_draw(self) -> None:
        self.clear()

        self._maze.draw()
        
        self._player.draw()
        
        # for (i, live) in enumerate(self.player_lives_ui):
        #     if i >= self._player.current_lives:
        #         live.alpha = 0

        # self.player_lives_ui.draw()
        
        for ghost in self._ghosts:
            ghost.draw()

        first_cell_pos = self._maze.get_cell(0, 0)

        if first_cell_pos.center:
            c_y = first_cell_pos.center.y
            time = arcade.Text(
                f"time: {int(self._time_to_finish)}",
                self._player._default_position.x - 100, c_y + 100)
            time.draw()

        self.score_ui.score_text.draw()
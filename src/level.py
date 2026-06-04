import arcade

from entity.ghost import Ghost
from entity.player import Player
from maze import Maze
from views import MenuView, PauseView, EndGameView


class Level(arcade.View):
    def __init__(self, player: Player, maze: Maze, ghosts: list[Ghost], time_to_finish: int, menu_view: MenuView) -> None:
        super().__init__()

        self._player = player
        self._maze = maze
        self._time_accumulator: float = 0
        self._time_to_finish= time_to_finish
        self._ghosts = ghosts
        self.menu_view = menu_view

    def on_update(self, delta_time: float) -> None:
        self._fixed_update(delta_time)

    def _fixed_update(self, delta_time: float) -> None:
        self._time_accumulator += delta_time
        time_step: float = 1 / 60

        while self._time_accumulator >= time_step:
            if self._time_to_finish <= 0:
                self.window.show_view(EndGameView(False, self._player.score, self.menu_view))
                break

            if not self._maze.has_pacgums():
                self.window.show_view(EndGameView(True, self._player.score, self.menu_view))
                break

            if self._player.collide_with_ghosts(self._ghosts):
                self._player.take_damage()

                if not self._player.current_lives:
                    self.window.show_view(EndGameView(False, self._player.score, self.menu_view))
                    pass

                self.restart_entity_position()

            self._player.update(time_step)

            for ghost in self._ghosts:
                ghost.update(time_step)

            self._time_accumulator -= time_step
            self._time_to_finish -= time_step

    def restart_entity_position(self) -> None:
        self._player.restart_position()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._player.set_next_direction(key=symbol)

        if symbol == arcade.key.SPACE:
            # self.restart_entity_position()
            self.window.show_view(PauseView(self))
        elif symbol == arcade.key.ENTER:
            self._player.take_damage()

    def on_draw(self) -> None:
        self.clear()

        self._maze.draw()
        self._player.draw()
        for ghost in self._ghosts:
            ghost.draw()

        time = arcade.Text(f"time: {int(self._time_to_finish)}", self.window.width // 2, self.window.height // 2 + 300)
        time.draw()

import arcade

from entity.player import Player
from maze import Maze
from views import MenuView, PauseView


class Level(arcade.View):
    def __init__(self, player: Player, maze: Maze) -> None:
        super().__init__()

        self._player = player
        self._maze = maze
        self._time_accumulator: float = 0

    def on_update(self, delta_time: float) -> None:
        self._fixed_update(delta_time)

    def _fixed_update(self, delta_time: float) -> None:
        self._time_accumulator += delta_time
        time_step: float = 1 / 60

        while self._time_accumulator >= time_step:
           
            if not self._maze.has_pacgums():
                # go to next level
                break
                
            # if self._player.collide_with_ghost(ghosts):
            #    self._player.take_damage()
                # if not self._player.current_lives:
                #     # game_over
                #     pass
                # self.restart_entity_position()

            self._player.update(time_step)
       
            self._time_accumulator -= time_step
    
    def restart_entity_position(self) -> None:
        self._player.restart_position()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._player.set_next_direction(key=symbol)

        if symbol == arcade.key.SPACE:
            # self.restart_entity_position()
            self.window.show_view(PauseView(self))

    def on_draw(self) -> None:
        self.clear()

        self._maze.draw()
        self._player.draw()

from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
from button import Button
from enum import IntEnum

if TYPE_CHECKING:
    from game import Game

class ButtonIndex(IntEnum):
    START = 0
    EXIT = 1

class MenuView(arcade.View):
    def __init__(self, game: Game) -> None:
        super().__init__()

        self._game = game
        self._buttons: list[Button] = []
        self.current_button: Button
        self.buttons_len = 2
        self.current_button_idx: int = 0
        self._start_button: Button

        self.setup()

    @property
    def game(self) -> Game:
        return self._game

    @property
    def buttons(self) -> list[Button]:
        return self._buttons

    def setup(self) -> None:
        self._start_button = Button(
            "start",
            self.window.width // 2,
            self.window.height // 2 + 100,
            "assets/button/game01.png",
            self.game.start
        )

        def quit():
            print("quit")

        b1 = Button(
            "b1",
            self.window.width // 2,
            self.window.height // 2 + 200,
            "assets/button/b1.png",
            quit
        )

        self.buttons.append(self._start_button)
        self.buttons.append(b1)

        self.current_button = self.buttons[self.current_button_idx]

    def on_show_view(self) -> None:
        print("Menu View started")

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.UP | arcade.key.W:
                self.current_button_idx -= 1
            case arcade.key.DOWN | arcade.key.S:
                self.current_button_idx += 1
            case arcade.key.SPACE:
                self.buttons[self.current_button_idx].trigger()
                return

        self.current_button_idx %= self.buttons_len
        self.current_button.set_alpha(255)

        self.current_button = self.buttons[self.current_button_idx]
        self.current_button.set_alpha(200)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> bool | None:
        point = arcade.Vec2(x, y)

        if self._start_button.collide_with_point(point):
            self.current_button_idx = ButtonIndex.START
            self._start_button.set_alpha(200)
            self._start_button.trigger()

    def on_draw(self) -> None:
        """ Draw everything """
        self.clear()

        for button in self.buttons:
            button.draw()

class PauseView(arcade.View):
    def __init__(self,  previous_view: arcade.View) -> None:
        super().__init__()
        self._previous_view = previous_view
        self._resume_button: Button
    
    def resume(self) -> None:
        print("continue")
        self.window.show_view(self._previous_view)
    

    def on_show_view(self) -> None:
        self._resume_button = Button("resume", self.window.width // 2, self.window.height // 2 + 100, "assets/button/back01.png", self.resume)
    
    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            self._resume_button.trigger()

    def on_draw(self) -> bool | None:
        self.clear()

        self._previous_view.on_draw()
        self._resume_button.draw()

class EndGameView(arcade.View):
    def __init__(self, win: bool, score: int, menu_view: MenuView) -> None:
        self.win = win
        self.score = score
        self._menu_view = menu_view
        self._quit_button: Button
        self._menu_buttton: Button
    
    def on_show_view(self) -> None:
        pass
    
    def on_draw(self) -> bool | None:
        self.clear()
        pass


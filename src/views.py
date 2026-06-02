from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
import sys
from button import Button, ButtonIndex, ButtonGroup

if TYPE_CHECKING:
    from game import Game

class MenuView(arcade.View):
    def __init__(self, game: Game) -> None:
        super().__init__()

        self._game = game
        self._button_group: ButtonGroup = ButtonGroup(4)
        self.setup()

    @property
    def game(self) -> Game:
        return self._game

    def setup(self) -> None:
        start_button = Button(
            "start",
            self.window.width // 2,
            self.window.height // 2 + 100,
            "assets/button/start/start.png",
            self.game.start
        )
        
        start_button.set_alpha(200)
        start_button.set_scale(2)

        def quit():
            print("quit")
            sys.exit(0)

        exit = Button(
            "quit",
            self.window.width // 2,
            self.window.height // 2,
            "assets/button/quit/quit.png",
            quit
        )

        exit.set_scale(2)

        self._button_group.add_button(start_button)
        self._button_group.add_button(exit)

    def on_show_view(self) -> None:
        print("Menu View started")

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> bool | None:
        self._button_group.on_mouse_press(x, y)
       
    
    # def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
    #     pass

    def on_draw(self) -> None:
        """ Draw everything """
        self.clear()
        self._button_group.draw()

class PauseView(arcade.View):
    def __init__(self, previous_view: arcade.View) -> None:
        super().__init__()
        self._previous_view = previous_view
        self._resume_button: Button

    def resume(self) -> None:
        print("continue")
        self.window.show_view(self._previous_view)

    def on_show_view(self) -> None:
        self._resume_button = Button(
            "resume",
            self.window.width // 2,
            self.window.height // 2 + 100,
            "assets/button/back01.png",
            self.resume)

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            self._resume_button.trigger()

    def on_draw(self) -> bool | None:
        self.clear()

        self._previous_view.on_draw()
        self._resume_button.draw()


class EndGameView(arcade.View):
    def __init__(self, win: bool, score: int, menu_view: MenuView) -> None:
        super().__init__()
        self.text = "Win" if win else "Game Over"
        self.score = score
        self._menu_view = menu_view
        self._button_group: ButtonGroup = ButtonGroup(2)

    def on_show_view(self) -> None:
        menu_buttton = Button(
            "menu_button",
            self.window.width // 2,
            self.window.height // 2 + 100,
            "assets/button/menu/menu.png",
            lambda: self.window.show_view(
                self._menu_view))
        
        menu_buttton.set_alpha(200)
        menu_buttton.set_scale(2)
        
        quit_button = Button("quit", 
            self.window.width // 2,
            self.window.height // 2, "assets/button/quit/quit.png", lambda: sys.exit(0))
        
        quit_button.set_scale(2)
        self._button_group.add_button(menu_buttton)
        self._button_group.add_button(quit_button)
        
        # open save score to get the highscore
        # check if score > highscore change highscore else do nothing
    
    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        self._button_group.on_key_press(key=symbol)
    
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int) -> bool | None:
        self._button_group.on_mouse_press(x, y)

    def on_draw(self) -> bool | None:
        self.clear()

        self._button_group.draw()
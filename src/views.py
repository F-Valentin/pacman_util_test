from __future__ import annotations
from typing import TYPE_CHECKING
import arcade
import hjson

from highscore import update_highscore_file
from button import Button, CheckButton, ButtonGroup
from cheatmode import CheatMode

"""Menu, pause, and end-of-game views used by the Arcade window."""

if TYPE_CHECKING:
    from game import Game


class MenuView(arcade.View):
    """Show the main menu with start and quit actions."""

    def __init__(self, game: Game) -> None:
        super().__init__()

        self._game = game
        self._button_group: ButtonGroup = ButtonGroup(4)

    @property
    def game(self) -> Game:
        return self._game

    def on_show_view(self) -> None:
        """Create the menu buttons and wire them to their handlers."""
        start_button = Button(
            "start",
            self.window.width // 2,
            self.window.height // 2 + 100,
            ["assets/button/start/start.png"],
            self.game.start
        )

        start_button.set_alpha(200)
        start_button.set_scale(2)

        exit_btn = Button(
            "quit",
            self.window.width // 2,
            self.window.height // 2 + 300,
            ["assets/button/quit/quit.png"],
            lambda: arcade.exit()
        )

        exit_btn.set_scale(2)

        instruction = Button(
            "instruction",
            self.window.width // 2,
            self.window.height // 2 + 200,
            ["assets/Single PNGs/ENTER.png"],
            lambda: self.window.show_view(InstructionView(self))
        )

        self._button_group.add_button(start_button)
        self._button_group.add_button(instruction)
        self._button_group.add_button(exit_btn)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._button_group.on_mouse_motion(x, y)

    def on_draw(self) -> None:
        """Draw everything."""
        self.clear()
        self._button_group.draw()


class PauseView(arcade.View):
    """Display the pause overlay and allow the player to resume."""

    def __init__(self, previous_view: arcade.View,
                 cheat_mode: CheatMode) -> None:
        super().__init__()
        self._previous_view = previous_view
        self._cheat_mode = cheat_mode
        self._resume_button: Button
        self._button_group: ButtonGroup = ButtonGroup(4)

    def resume(self) -> None:
        print("continue")
        self.window.show_view(self._previous_view)

    def on_show_view(self) -> None:
        # Bouton Resume
        self._resume_button = Button(
            "resume",
            self.window.width // 2,
            self.window.height // 2 + 100,
            ["assets/button/back01.png"],
            self.resume
        )
        self._resume_button.set_scale(0.4)

        cheat_group = self._cheat_mode.button_group

        self._button_group.add_button(self._resume_button)

        for btn in cheat_group._buttons:
            self._button_group.add_button(btn)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._button_group.on_mouse_motion(x, y)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

    def on_draw(self) -> None:
        self.clear()
        self._previous_view.on_draw()
        self._button_group.draw()


class EndGameView(arcade.View):
    """Show the outcome of the session and return to the menu."""

    def __init__(self, win: bool, score: int,
                 menu_view: MenuView) -> None:
        super().__init__()
        self.text = "Win" if win else "Game Over"
        self.score = score
        self.highscore = 0
        self._menu_view = menu_view
        self._button_group: ButtonGroup = ButtonGroup(2)

    def on_show_view(self) -> None:
        menu_button = Button(
            "menu_button",
            self.window.width // 2,
            self.window.height // 2 + 100,
            ["assets/button/menu/menu.png"],
            lambda: self.window.show_view(self._menu_view)
        )

        menu_button.set_alpha(200)
        menu_button.set_scale(2)

        quit_button = Button(
            "quit",
            self.window.width // 2,
            self.window.height // 2,
            ["assets/button/quit/quit.png"],
            lambda: arcade.exit()
        )

        quit_button.set_scale(2)
        self._button_group.add_button(menu_button)
        self._button_group.add_button(quit_button)

        highscore = 0
        try:
            with open("highscore.json", 'r', encoding='utf-8') as f:
                print("open")
                data = hjson.load(f)
                highscore = data.get("highscore", 0)
                self.highscore = highscore
        except (FileNotFoundError, hjson.HjsonDecodeError) as e:
            print(e)

        if self.score > highscore:
            print("update")
            update_highscore_file("highscore.json", self.score)
            self.highscore = self.score

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

    def on_draw(self) -> None:
        self.clear()

        result_text = arcade.Text(
            f"{self.text}  —  Score : {self.score}",
            self.window.width // 2,
            self.window.height // 2 + 220,
            anchor_x="center",
        )
        result_text.draw()

        highscore_text = arcade.Text(
            f"HighScore : {self.highscore}",
            self.window.width // 2,
            self.window.height // 2 + 120,
            anchor_x="center",
        )

        highscore_text.draw()
        self._button_group.draw()


class InstructionView(arcade.View):
    def __init__(self, menu_view: MenuView) -> None:
        super().__init__()
        from arcade import Sprite
        self._button_group: ButtonGroup = ButtonGroup(2)
        self._menu_view = menu_view

        pos_d = arcade.Vec2(
            self.window.width // 2 + 100, self.window.height // 2)
        pos_r = arcade.Vec2(pos_d.x + 20, pos_d.y)
        pos_l = arcade.Vec2(pos_d.x - 20, pos_d.y)
        pos_u = arcade.Vec2(pos_d.x, pos_d.y + 20)

        arrow_d = Sprite("assets/Single PNGs/ARROWDOWN.png",
                         1, pos_d.x, pos_d.y)
        arrow_l = Sprite("assets/Single PNGs/ARROWLEFT.png",
                         1, pos_l.x, pos_l.y)
        arrow_r = Sprite("assets/Single PNGs/ARROWRIGHT.png",
                         1, pos_r.x, pos_r.y)
        arrow_u = Sprite("assets/Single PNGs/ARROWUP.png",
                         1, pos_u.x, pos_u.y)

        self.move_wasd = arcade.Text(
            "You can move using the key arrows or wasd",
            pos_l.x - 20, pos_u.y + 20)
        self.arrows: arcade.SpriteList = arcade.SpriteList()
        self.arrows.append(arrow_d)
        self.arrows.append(arrow_l)
        self.arrows.append(arrow_r)
        self.arrows.append(arrow_u)

        skip_level = CheckButton(
            "skip level",
            pos_r.x + 50, pos_u.y,
            ["assets/button/checkbutton.png",
             "assets/button/uncheckbutton.png"]
        )
        skip_level.set_scale(0.1)

        quit_button = Button(
            "quit",
            self.window.width // 2,
            self.window.height // 2,
            ["assets/button/quit/quit.png"],
            lambda: self.window.show_view(self._menu_view)
        )

        self._button_group.add_button(quit_button)
        self._button_group.add_button(skip_level)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._button_group.on_mouse_motion(x, y)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

    def on_draw(self) -> None:
        self.clear()
        text = arcade.Text(
            "instruction",
            self.window.width // 2,
            self.window.height // 2 + 200)
        self.arrows.draw()
        self._button_group.draw()
        self.move_wasd.draw()
        text.draw()

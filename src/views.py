from __future__ import annotations

from typing import TYPE_CHECKING

import arcade
import hjson

from button import Button, ButtonGroup
from cheatmode import CheatMode, compute_panel_bounds
from paths import persistent_path
from utils import HitBox

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
        btn_w = 200
        btn_h = 50
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        start_button = Button(
            "Start",
            center_x,
            center_y + 150,
            btn_w, btn_h,
            self.game.start
        )
        start_button.set_alpha(200)

        instruction = Button(
            "Instruction",
            center_x,
            center_y + 50,
            btn_w, btn_h,
            lambda: self.window.show_view(InstructionView(self))
        )

        top_highscore = Button(
            "Top Highscore",
            center_x,
            center_y - 50,
            btn_w, btn_h,
            lambda: self.window.show_view(TopHighscoreView(self))
        )

        exit_btn = Button(
            "Quit",
            center_x,
            center_y - 150,
            btn_w, btn_h,
            lambda: arcade.exit()
        )

        self._button_group.add_button(start_button)
        self._button_group.add_button(instruction)
        self._button_group.add_button(top_highscore)
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
                 cheat_mode: CheatMode, menu_view: MenuView) -> None:
        super().__init__()
        self._previous_view = previous_view
        self._cheat_mode = cheat_mode
        self._menu_view = menu_view
        self._resume_button: Button
        self._button_group: ButtonGroup = ButtonGroup(5)
        self._panel_rect: arcade.types.Rect | None = None

    def resume(self) -> None:
        self.window.show_view(self._previous_view)

    def on_show_view(self) -> None:
        btn_w = 150
        btn_h = 40

        self._resume_button = Button(
            "Resume",
            self.window.width // 2,
            self.window.height // 2 + 100,
            btn_w, btn_h,
            self.resume
        )

        back_button = Button(
            "Menu",
            self.window.width // 2,
            self.window.height // 2 + 150,
            btn_w, btn_h,
            lambda: self.window.show_view(self._menu_view)
        )
        cheat_group_buttons = self._cheat_mode.buttons

        self._button_group.add_button(back_button)
        self._button_group.add_button(self._resume_button)

        for btn in cheat_group_buttons:
            self._button_group.add_button(btn)

        self._panel_rect = compute_panel_bounds(
            self._button_group.buttons,
            self._cheat_mode.labels,
            padding=20,
        )

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

        if self._panel_rect is not None:
            arcade.draw_rect_filled(self._panel_rect, arcade.color.BLACK)
            arcade.draw_rect_outline(
                self._panel_rect,
                arcade.color.WHITE,
                border_width=2)

        self._cheat_mode.draw()
        self._button_group.draw()


class EndGameView(arcade.View):
    """Show the outcome of the session and return to the menu."""
    BOX_LEFT = 75
    BOX_RIGHT = 360
    BOX_TOP = 720
    BOX_BOTTOM = 530

    def __init__(self, win: bool, score: int,
                 menu_view: MenuView) -> None:
        super().__init__()
        self.text: str = "Win" if win else "Game Over"
        self.score: int = score
        self.highscore: int = 0
        self._menu_view: MenuView = menu_view
        self._button_group: ButtonGroup = ButtonGroup(3)
        self.current_name: str = ""
        self.old_name: str = ""
        self.enter_your_name_btn_pressed: bool = False
        self.data: dict[str, int] = {}
        self.tmp_data: dict[str, int] = {}

        self._input_rect: HitBox

    def on_show_view(self) -> None:
        btn_x = 160
        btn_w = 150
        btn_h = 40

        label = arcade.Text(
            "Enter your name :",
            self.BOX_LEFT,
            0,
            font_size=13)
        rect_x = self.BOX_LEFT + label.content_width + 5
        self._input_rect = HitBox(
            x=rect_x,
            y=self.BOX_BOTTOM - 55,
            width=160,
            height=20)

        menu_button = Button(
            "Menu",
            btn_x,
            350,
            btn_w, btn_h,
            lambda: (self.window.show_view(self._menu_view), self.save_highscore())
        )
        menu_button.set_alpha(200)

        quit_button = Button(
            "Quit",
            btn_x,
            260,
            btn_w, btn_h,
            lambda: (self.save_highscore(), arcade.exit())
        )

        path = persistent_path("highscore.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = hjson.load(f)
                self.data = data
        except (FileNotFoundError, hjson.HjsonDecodeError) as e:
            print(e)

        self._button_group.add_button(menu_button)
        self._button_group.add_button(quit_button)

    def save_highscore(self) -> None:
        path = persistent_path("highscore.json")

        values: list[int] = list(self.data.values())
        values.sort()

        min_key = ""

        self.highscore = self.data.get(self.current_name, self.score)

        self.highscore = max(self.score, self.highscore)

        if len(self.data) + 1 > 10:
            for (key, value) in self.data.items():
                if value == values[0]:
                    min_key = key
                    break

            if self.highscore <= values[0]:
                return

            del self.data[min_key]

        if self.current_name not in self.data and len(self.old_name) == 0:
            self.old_name = self.current_name

        self.enter_your_name_btn_pressed = False

        if len(self.old_name) > 0 and self.old_name != self.current_name:
            del self.data[self.old_name]
            self.old_name = ""

        self.data[self.current_name] = self.highscore

        with open(path, "w") as f:
            import json
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if not self.enter_your_name_btn_pressed:
            self._button_group.on_key_press(key=symbol)
            return

        if symbol == arcade.key.BACKSPACE and len(self.current_name) > 0:
            self.current_name = self.current_name[:-1]
        else:
            c = chr(symbol)
            if c.isalpha() and c.isascii() and len(self.current_name) < 10:
                self.current_name += c

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

        if self._input_rect.collide_with_point(arcade.Vec2(x, y)):
            self.enter_your_name_btn_pressed = True
        else:
            self.enter_your_name_btn_pressed = False

    def on_draw(self) -> None:
        self.clear()

        rect = arcade.LRBT(
            self.BOX_LEFT,
            self.BOX_RIGHT,
            self.BOX_BOTTOM,
            self.BOX_TOP)
        arcade.draw_rect_outline(rect, arcade.color.WHITE, border_width=2)

        arcade.Text(
            self.text,
            self.BOX_LEFT + 15, self.BOX_TOP - 45,
            font_size=18,
        ).draw()

        arcade.Text(
            f"Your score : {self.score}",
            self.BOX_LEFT + 15, self.BOX_TOP - 95,
            font_size=14,
        ).draw()

        arcade.Text(
            f"Your Highscore : {self.highscore}",
            self.BOX_LEFT + 15, self.BOX_TOP - 145,
            font_size=14,
        ).draw()

        arcade.Text(
            (
                "(type inside the rect oultine and then"
                "type any letter on your keyboard"
                "then press enter to save your score)"
            ),
            self.BOX_LEFT, self.BOX_BOTTOM - 28,
            font_size=10,
            color=arcade.color.LIGHT_GRAY,
        ).draw()

        label = arcade.Text(
            "Enter your name :",
            self.BOX_LEFT,
            self.BOX_BOTTOM - 70,
            font_size=13)
        label.draw()

        rect_x = self.BOX_LEFT + label.content_width + 5
        input_rect = arcade.LRBT(
            rect_x,
            rect_x + 160,
            self.BOX_BOTTOM - 75,
            self.BOX_BOTTOM - 55)
        arcade.draw_rect_outline(
            input_rect,
            arcade.color.WHITE,
            border_width=2)

        arcade.Text(
            self.current_name,
            rect_x + 5,
            self.BOX_BOTTOM - 72,
            font_size=12).draw()
        self._button_group.draw()


class InstructionView(arcade.View):
    """Show the game controls as simple text."""

    CONTROLS: list[str] = [
        "Move: Arrow Keys or WASD",
        "Pause: SPACE",
    ]

    def __init__(self, menu_view: MenuView) -> None:
        super().__init__()
        self._menu_view = menu_view
        self._button_group: ButtonGroup = ButtonGroup(1)

        center_x = self.window.width // 2
        center_y = self.window.height // 2

        self._title = arcade.Text(
            "Instructions",
            center_x,
            center_y + 150,
            font_size=24,
            anchor_x="center",
        )

        self._lines: list[arcade.Text] = [
            arcade.Text(
                line,
                center_x,
                center_y + 70 - (i * 40),
                font_size=16,
                anchor_x="center",
            )
            for i, line in enumerate(self.CONTROLS)
        ]

        back_button = Button(
            "back",
            center_x,
            center_y - 150,
            150, 40,
            lambda: self.window.show_view(self._menu_view)
        )
        self._button_group.add_button(back_button)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._button_group.on_mouse_motion(x, y)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

    def on_draw(self) -> None:
        self.clear()
        self._title.draw()
        for line in self._lines:
            line.draw()
        self._button_group.draw()


class TopHighscoreView(arcade.View):
    def __init__(self, menu_view: MenuView) -> None:
        super().__init__()
        self._menu_view = menu_view
        self._button_group: ButtonGroup = ButtonGroup(1)
        self._labels: list[arcade.Text] = []
        self._back_button: Button | None = None

    def on_show_view(self) -> None:
        path = persistent_path("highscore.json")
        data: dict[str, int] = {}

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = hjson.load(f)
        except (FileNotFoundError, hjson.HjsonDecodeError) as e:
            print(e)
            if not isinstance(data, dict):
                data = {}

        sorted_scores = sorted(
            [(name, score) for name, score in data.items()],
            key=lambda x: x[1],
            reverse=True
        )[:10]

        title_label = arcade.Text(
            "Top Highscore",
            self.window.width // 2,
            self.window.height - 80,
            font_size=24,
            anchor_x="center",
            color=arcade.color.WHITE
        )
        self._labels.append(title_label)

        start_y = self.window.height - 160
        y_pos = 0
        for idx, (name, score) in enumerate(sorted_scores):
            y_pos = start_y - (idx * 30)
            label = arcade.Text(
                f"{name}: {score}",
                self.window.width // 2,
                y_pos,
                font_size=16,
                anchor_x="center",
                color=arcade.color.WHITE
            )
            self._labels.append(label)

        if not sorted_scores:
            y_pos = self.window.height // 2
            label = arcade.Text(
                "No scores recorded yet!",
                self.window.width // 2,
                y_pos,
                font_size=16,
                anchor_x="center",
                color=arcade.color.LIGHT_GRAY
            )
            self._labels.append(label)

        self._back_button = Button(
            "Menu",
            self.window.width // 2,
            y_pos - 100,
            150, 40,
            lambda: self.window.show_view(self._menu_view)
        )
        self._button_group.add_button(self._back_button)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> None:
        self._button_group.on_mouse_motion(x, y)

    def on_mouse_press(self, x: int, y: int, button: int,
                       modifiers: int) -> None:
        self._button_group.on_mouse_press(x, y)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self._button_group.on_key_press(key=symbol)

    def on_draw(self) -> None:
        self.clear()

        for label in self._labels:
            label.draw()

        if self._back_button:
            self._back_button.draw()

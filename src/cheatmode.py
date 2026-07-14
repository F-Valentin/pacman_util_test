from typing import Callable
import arcade
from button import CheckButton, ButtonGroup


class CheatMode:
    def __init__(self, window: arcade.Window) -> None:
        self.player_inviciblity: Callable
        self.ghosts_freeze: list[Callable] = []
        self.can_skip_levels: Callable

        self._window = window
        self._button_group: ButtonGroup = ButtonGroup(3)
        self._buttons_initialized: bool = False

    def _init_buttons(self) -> None:
        if self._buttons_initialized:
            return

        center_x = self._window.width // 2
        base_y = self._window.height // 2

        skip_btn = CheckButton(
            "skip_level",
            center_x,
            base_y,
            ["assets/button/uncheckbutton.png", "assets/button/checkbutton.png"],
            target=self.can_skip_levels
        )
        skip_btn.set_scale(0.1)

        invincible_btn = CheckButton(
            "invincibility",
            center_x,
            base_y - 60,
            ["assets/button/uncheckbutton.png", "assets/button/checkbutton.png"],
            target=self.player_inviciblity
        )
        invincible_btn.set_scale(0.1)

        freeze_btn = CheckButton(
            "freeze_ghosts",
            center_x,
            base_y - 120,
            ["assets/button/uncheckbutton.png", "assets/button/checkbutton.png"],
            target=self._freeze_all
        )
        freeze_btn.set_scale(0.1)

        self._button_group.add_button(skip_btn)
        self._button_group.add_button(invincible_btn)
        self._button_group.add_button(freeze_btn)

        self._buttons_initialized = True

    def _freeze_all(self) -> None:
        for freeze in self.ghosts_freeze:
            freeze()

    @property
    def button_group(self) -> ButtonGroup:
        if not self._buttons_initialized:
            self._init_buttons()
        return self._button_group

    def draw(self) -> None:
        if not self._buttons_initialized:
            self._init_buttons()
        self._button_group.draw()

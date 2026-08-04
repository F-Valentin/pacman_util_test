from collections.abc import Callable

import arcade

from button import Button, ButtonGroup, CheckButton


def compute_panel_bounds(
    buttons: list[Button],
    labels: list[arcade.Text] | None = None,
    padding: float = 20,
) -> arcade.types.Rect:
    """Compute a padded bounding rect that encloses all given buttons/labels.

    Flexible by design: pass whatever buttons and labels currently exist
    (e.g. group.buttons, cheat_mode.labels) and the returned rect grows or
    shrinks to fit them - no hardcoded menu size to maintain.
    """
    labels = labels or []
    lefts: list[float] = []
    rights: list[float] = []
    bottoms: list[float] = []
    tops: list[float] = []

    for button in buttons:
        half_w = button.width / 2
        half_h = button.height / 2
        lefts.append(button.center.x - half_w)
        rights.append(button.center.x + half_w)
        bottoms.append(button.center.y - half_h)
        tops.append(button.center.y + half_h)

    for label in labels:
        lefts.append(label.left)
        rights.append(label.right)
        bottoms.append(label.bottom)
        tops.append(label.top)

    if not lefts:
        return arcade.LRBT(0, 0, 0, 0)

    return arcade.LRBT(
        min(lefts) - padding,
        max(rights) + padding,
        min(bottoms) - padding,
        max(tops) + padding,
    )


class CheatMode:
    def __init__(self, window: arcade.Window) -> None:
        self.player_inviciblity: Callable
        self.ghosts_freeze: list[Callable] = []
        self.can_skip_levels: Callable

        self._window = window
        self._button_group: ButtonGroup = ButtonGroup(3)
        self._buttons_initialized: bool = False
        self._labels: list[arcade.Text] = []

    def _add_label(self, text: str, x: float, y: float) -> None:
        label = arcade.Text(
            text,
            x,
            y,
            color=arcade.color.WHITE,
            font_size=12,
            anchor_x="center",
            anchor_y="bottom",
        )
        self._labels.append(label)

    def _init_buttons(self) -> None:
        if self._buttons_initialized:
            return

        center_x = self._window.width // 2
        base_y = self._window.height // 2
        label_offset = 25

        skip_btn = CheckButton(
            "skip_level",
            center_x,
            base_y,
            ["assets/button/uncheckbutton.png", "assets/button/checkbutton.png"],
            target=self.can_skip_levels
        )
        skip_btn.set_scale(0.1)
        self._add_label("Skip Level", center_x, base_y + label_offset)

        invincible_btn = CheckButton(
            "invincibility",
            center_x,
            base_y - 60,
            ["assets/button/uncheckbutton.png", "assets/button/checkbutton.png"],
            target=self.player_inviciblity
        )
        invincible_btn.set_scale(0.1)
        self._add_label("Invincibility", center_x, base_y - 60 + label_offset)

        freeze_btn = CheckButton(
            "freeze_ghosts",
            center_x,
            base_y - 120,
            ["assets/button/uncheckbutton.png", "assets/button/checkbutton.png"],
            target=self._freeze_all
        )
        freeze_btn.set_scale(0.1)
        self._add_label("Freeze Ghosts", center_x, base_y - 120 + label_offset)

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

    @property
    def labels(self) -> list[arcade.Text]:
        if not self._buttons_initialized:
            self._init_buttons()
        return self._labels

    def draw(self) -> None:
        if not self._buttons_initialized:
            self._init_buttons()
        self._button_group.draw()
        for label in self._labels:
            label.draw()
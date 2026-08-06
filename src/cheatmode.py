from collections.abc import Callable

import arcade

from button import Button, CheckButton


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
        self._buttons: list[Button] = []
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
        
        btn_w = 40
        btn_h = 40
        padding = 30
        step_y = btn_h + padding
        label_offset = btn_h / 2 + 5  # Place label just above the button

        skip_btn = CheckButton(
            "skip_level",
            center_x,
            base_y,
            btn_w, btn_h,
            target=self.can_skip_levels
        )
        self._buttons.append(skip_btn)
        self._add_label("Skip Level", center_x, base_y + label_offset)

        invincible_btn = CheckButton(
            "invincibility",
            center_x,
            base_y - step_y,
            btn_w, btn_h,
            target=self.player_inviciblity
        )
        self._buttons.append(invincible_btn)
        self._add_label("Invincibility", center_x, base_y - step_y + label_offset)

        freeze_btn = CheckButton(
            "freeze_ghosts",
            center_x,
            base_y - 2 * step_y,
            btn_w, btn_h,
            target=self._freeze_all
        )
        self._buttons.append(freeze_btn)
        self._add_label("Freeze Ghosts", center_x, base_y - 2 * step_y + label_offset)

        self._buttons_initialized = True

    def _freeze_all(self) -> None:
        for freeze in self.ghosts_freeze:
            freeze()

    @property
    def buttons(self) -> list[Button]:
        if not self._buttons_initialized:
            self._init_buttons()
        return self._buttons

    @property
    def labels(self) -> list[arcade.Text]:
        if not self._buttons_initialized:
            self._init_buttons()
        return self._labels

    def draw(self) -> None:
        for label in self._labels:
            label.draw()
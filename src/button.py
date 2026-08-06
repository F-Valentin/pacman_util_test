from collections.abc import Callable

import arcade

from utils import HitBox


class Button:
    def __init__(self, name: str, x: float, y: float,
                 width: float, height: float,
                 trigger: Callable | None = None,
                 background_color: tuple[int, int, int, int] = (0, 0, 0, 255),
                 border_color: tuple[int, int, int, int] = (255, 255, 255, 255),
                 border_width: int = 2) -> None:
        self._name = name
        self.center: arcade.Vec2 = arcade.Vec2(x, y)
        self._width = width
        self._height = height
        self._background_color = background_color
        self._border_color = border_color
        self._border_width = border_width
        self._alpha = 255
        self._scale = 1.0

        self._trigger = trigger if trigger else lambda: ()
        self._update_collision_rect()

    def _update_collision_rect(self) -> None:
        w = self._width * self._scale
        h = self._height * self._scale
        top_left_x = self.center.x - w / 2
        top_left_y = self.center.y + h / 2
        self.collision_rect: HitBox = HitBox(top_left_x, top_left_y, w, h)

    def _draw_background(self) -> None:
        rect = arcade.LRBT(
            self.center.x - self.width / 2,
            self.center.x + self.width / 2,
            self.center.y - self.height / 2,
            self.center.y + self.height / 2
        )
        
        r, g, b, a = self._background_color
        bg_color = (r, g, b, int(self._alpha * (a / 255)))
        
        r, g, b, a = self._border_color
        border_color = (r, g, b, int(self._alpha * (a / 255)))

        arcade.draw_rect_filled(rect, bg_color)
        if self._border_width > 0:
            arcade.draw_rect_outline(rect, border_color, self._border_width)

    @property
    def name(self) -> str:
        return self._name

    @property
    def trigger(self) -> Callable:
        return self._trigger

    @property
    def width(self) -> float:
        return self._width * self._scale

    @property
    def height(self) -> float:
        return self._height * self._scale

    def set_alpha(self, value: int) -> None:
        self._alpha = value

    def set_scale(self, value: float) -> None:
        self._scale = value
        self._update_collision_rect()

    def draw(self) -> None:
        self._draw_background()

        r, g, b, a = arcade.color.WHITE
        text_color = (r, g, b, int(self._alpha * (a / 255)))
        
        arcade.Text(
            self._name,
            self.center.x,
            self.center.y,
            color=text_color,
            font_size=max(10, int(self.height / 4)),
            anchor_x="center",
            anchor_y="center"
        ).draw()


class CheckButton(Button):
    def __init__(self, name: str, x: float, y: float,
                 width: float, height: float,
                 trigger: Callable | None = None,
                 target: Callable | None = None,
                 background_color: tuple[int, int, int, int] = (0, 0, 0, 255),
                 border_color: tuple[int, int, int, int] = (255, 255, 255, 255),
                 border_width: int = 2) -> None:
        self._check = False
        self.target = target
        actual_trigger = trigger if trigger else lambda: self.check()
        
        super().__init__(name, x, y, width, height, actual_trigger,
                         background_color, border_color, border_width)

    def check(self) -> None:
        self._check = not self._check
        if self.target:
            self.target()

    def draw(self) -> None:
        # Only draw the background and border, skip drawing the name
        self._draw_background()
        
        if self._check:
            w = self.width * 0.3
            h = self.height * 0.3
            cx = self.center.x
            cy = self.center.y
            
            r, g, b, a = arcade.color.WHITE
            line_color = (r, g, b, int(self._alpha * (a / 255)))

            # Two lines to create the V-shape
            arcade.draw_line(
                cx - w / 2, cy - h / 4,
                cx, cy - h / 2,
                line_color, 2
            )
            arcade.draw_line(
                cx, cy - h / 2,
                cx + w / 2, cy + h / 2,
                line_color, 2
            )


class ButtonGroup:
    def __init__(self, capacity: int) -> None:
        self._buttons: list[Button] = []
        self.size: int = 0
        self.capacity: int = capacity
        self.current_button_idx: int = 0
        self.current_button_focus: Button | None = None

    @property
    def buttons(self) -> list[Button]:
        return self._buttons

    def add_button(self, button: Button) -> bool:
        if not self.size:
            self.current_button_focus = button
            button.set_alpha(200)
        if self.size < self.capacity:
            self._buttons.append(button)
            self.size += 1
            return True
        return False

    def set_default_button(self, button: Button, idx: int) -> None:
        self.current_button_focus = button
        self.current_button_idx = idx

    def on_key_press(self, key: int) -> None:
        old_current_button_idx: int = self.current_button_idx

        match key:
            case arcade.key.UP | arcade.key.W:
                self.current_button_idx -= 1
            case arcade.key.DOWN | arcade.key.S:
                self.current_button_idx += 1
            case arcade.key.SPACE:
                if self.size and self.current_button_focus:
                    self.current_button_focus.trigger()
                return

        if self.size:
            old_button: Button = self._buttons[old_current_button_idx]
            old_button.set_alpha(255)
            self.current_button_idx %= self.size
            button: Button = self._buttons[self.current_button_idx]
            button.set_alpha(200)
            self.current_button_focus = button

    def on_mouse_press(self, x: int, y: int) -> None:
        """Vérifie TOUS les boutons, pas seulement le focus."""
        point = arcade.Vec2(x, y)
        for button in self._buttons:
            if button.collision_rect.collide_with_point(point):
                button.trigger()

                if self.current_button_focus and self.current_button_focus != button:
                    self.current_button_focus.set_alpha(255)

                self.current_button_focus = button
                button.set_alpha(200)
                self.current_button_idx = self._buttons.index(button)
                return

    def on_mouse_motion(self, x: int, y: int) -> None:
        point = arcade.Vec2(x, y)
        for idx, button in enumerate(self._buttons):
            if button.collision_rect.collide_with_point(point):
                if (self.current_button_focus
                        and self.current_button_focus != button):
                    self.current_button_focus.set_alpha(255)
                self.current_button_focus = button
                button.set_alpha(200)
                self.current_button_idx = idx
                return

    def draw(self) -> None:
        for button in self._buttons:
            button.draw()
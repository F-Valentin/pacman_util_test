from collections.abc import Callable

import arcade

from utils import HitBox


class Button:
    def __init__(self, name: str, x: float, y: float,
                 path_to_images: list[str], trigger: Callable | None = None
                 ) -> None:
        self._name = name
        self.center: arcade.Vec2 = arcade.Vec2(x, y)
        self._sprite_list: arcade.SpriteList = arcade.SpriteList()

        for image in path_to_images:
            sprite = arcade.Sprite(image)
            sprite.position = self.center
            self._sprite_list.append(sprite)

        self._trigger = trigger if trigger else lambda: ()
        self._current_sprite_idx = 0
        self._update_collision_rect()

    def _update_collision_rect(self) -> None:
        sprite = self._sprite_list[0] if len(self._sprite_list) > 0 else None
        if sprite is None:
            return
        top_left_x = self.center.x - sprite.width // 2
        top_left_y = self.center.y + sprite.height // 2
        self.collision_rect: HitBox = HitBox(
            top_left_x, top_left_y, sprite.width, sprite.height)
        self._sprite = sprite

    @property
    def name(self) -> str:
        return self._name

    @property
    def trigger(self) -> Callable:
        return self._trigger

    @property
    def width(self) -> float:
        return self._sprite.width if self._sprite else 0.0

    @property
    def height(self) -> float:
        return self._sprite.height if self._sprite else 0.0

    def set_alpha(self, value: int) -> None:
        for sprite in self._sprite_list:
            sprite.alpha = value

    def set_scale(self, value: float) -> None:
        for sprite in self._sprite_list:
            sprite.scale = value
        self._update_collision_rect()

    def draw(self) -> None:
        self._sprite_list.draw()


class CheckButton(Button):
    def __init__(self, name: str, x: float, y: float,
                 path_to_images: list[str], trigger: Callable | None = None,
                 target: Callable | None = None) -> None:
        self._check = False
        self.target = target
        self._tmp_sprite_list: arcade.SpriteList = arcade.SpriteList()

        for image in path_to_images:
            sprite = arcade.Sprite(image)
            sprite.position = arcade.Vec2(x, y)
            self._tmp_sprite_list.append(sprite)

        actual_trigger = trigger if trigger else lambda: self.check()

        super().__init__(name, x, y,
                         [path_to_images[0]] if path_to_images else [],
                         actual_trigger)

    def check(self) -> None:
        self._check = not self._check

        idx = 1 if self._check else 0
        if idx < len(self._tmp_sprite_list):
            new_sprite = self._tmp_sprite_list[idx]
            new_sprite.position = self.center
            new_sprite.scale = self._sprite.scale
            new_sprite.alpha = self._sprite.alpha

            self._sprite_list.clear()
            self._sprite_list.append(new_sprite)
            self._sprite = new_sprite
            self._update_collision_rect()

        if self.target:
            self.target()


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

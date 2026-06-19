import arcade
from utils import Rect
from collections.abc import Callable
from typing import Optional
from enum import IntEnum

class ButtonIndex(IntEnum):
    """Named indexes for menu and overlay buttons."""
    START = 0
    RESUME = 1
    OPTION = 2
    QUIT = 3

class Button:
    """Wrap an Arcade sprite and its click/keyboard activation callback."""

    def __init__(self, name: str, x: float, y: float,
                 path_to_image: str, trigger: Callable) -> None:
        self._name = name

        self.center: arcade.Vec2 = arcade.Vec2(x, y)

        self._sprite: arcade.Sprite = arcade.Sprite(path_to_image)
        self._sprite_list = arcade.SpriteList()
        self._sprite.position = self.center
        self._sprite_list.append(self._sprite)

        self.trigger = trigger

        top_left_x = x - self._sprite.width // 2
        top_left_y = y + self._sprite.height // 2

        self.collision_rect: Rect = Rect(
            top_left_x,
            top_left_y,
            self._sprite.width,
            self._sprite.height)


    @property
    def name(self) -> str:
        return self._name

    def set_alpha(self, value: int) -> None:
        """Set the button sprite transparency for highlighted states."""
        self._sprite.alpha = value
    
    def set_scale(self, value: int) -> None:
        """Scale the button sprite to match the current UI layout."""
        self._sprite.scale = value

    def draw(self) -> None:
        self._sprite_list.draw()

    def collide_with_point(self, point: arcade.Vec2) -> bool:
        """Return whether the given point is inside the button bounds."""
        rect = self.collision_rect

        if (
            point.x < rect.x or point.x > rect.x + rect.width
            or point.y > rect.y or point.y < rect.y - rect.height
        ):
            return False

        return True

class ButtonGroup:
    """Manage a small set of buttons for keyboard and mouse input."""

    def __init__(self, capacity: int) -> None:
        self._buttons: list[Button] = []
        self.size: int = 0
        self.capacity: int = capacity

        self.current_button_idx: int = 0
        self.current_button_focus: Optional[Button] = None
    
    def add_button(self, button: Button) -> bool:
        """Append a button if there is room in the group."""
        if not self.size:
            self.current_button_focus = button

        if self.size < self.capacity:
            self._buttons.append(button)
            self.size += 1
        else:
            return False
        
        return True
    
    def set_default_button(self, button: Button, idx: int) -> None:
        self.current_button_focus = button
        self.current_button_idx = idx
    
    def on_key_press(self, key: int) -> None:
        """Move the focus between buttons or trigger the selected one."""
        old_current_button_idx: int = self.current_button_idx

        match key:
            case arcade.key.UP | arcade.key.W:
                self.current_button_idx -= 1
            case arcade.key.DOWN | arcade.key.S:
                self.current_button_idx += 1
            case arcade.key.SPACE:
                if self.size:
                    self.current_button_focus.trigger()

                return

        old_button: Button = self._buttons[old_current_button_idx]
        old_button.set_alpha(255)

        self.current_button_idx %= self.size

        button: Button = self._buttons[self.current_button_idx]        
        button.set_alpha(200)
        self.current_button_focus = button

    def on_mouse_press(self, x: int, y: int) -> None:
        """Activate the first button that contains the clicked point."""
        if self.current_button_focus:
            point = arcade.Vec2(x, y)
            if self.current_button_focus.collide_with_point(point):
                self.current_button_focus.trigger() 

    def on_mouse_motion(self, x: int, y: int) -> None:
        point = arcade.Vec2(x, y)

        for (idx, button) in enumerate(self._buttons):
            if button.collide_with_point(point):
                print("collide")
                self.current_button_focus.set_alpha(255)
                self.current_button_focus = button
                button.set_alpha(200)
                self.current_button_idx = idx

    def draw(self) -> None:
        for button in self._buttons:
            button.draw()
import arcade
from utils import Rect
from collections.abc import Callable
from enum import IntEnum

class ButtonIndex(IntEnum):
    START = 0
    RESUME = 1
    OPTION = 2
    QUIT = 3

class Button:
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
        self._sprite.alpha = value

    def draw(self) -> None:
        self._sprite_list.draw()

    def collide_with_point(self, point: arcade.Vec2) -> bool:
        rect = self.collision_rect

        if (
            point.x < rect.x or point.x > rect.x + rect.width
            or point.y > rect.y or point.y < rect.y - rect.height
        ):
            return False

        return True

class ButtonGroup:
    def __init__(self, capacity: int) -> None:
        self._buttons: list[Button] = []
        self.size: int = 0
        self.capacity: int = capacity

        self.current_button_idx: int = ButtonIndex.START
    
    def add_button(self, button: Button) -> bool:
        if self.size < self.capacity:
            self._buttons.append(button)
            self.size += 1
        else:
            return False
        
        return True
    
    def on_key_press(self, key: int) -> None:
        old_current_button_idx: int = self.current_button_idx

        match key:
            case arcade.key.UP | arcade.key.W:
                self.current_button_idx -= 1
            case arcade.key.DOWN | arcade.key.S:
                self.current_button_idx += 1
            case arcade.key.SPACE:
                if self.size:
                    self._buttons[self.current_button_idx].trigger()

                return

        old_button: Button = self._buttons[old_current_button_idx]
        old_button.set_alpha(255)

        self.current_button_idx %= self.size

        button: Button = self._buttons[self.current_button_idx]        
        button.set_alpha(200)

    def on_mouse_press(self, x: int, y: int) -> None:
        point = arcade.Vec2(x, y)

        for button in self._buttons:
            if button.collide_with_point(point):
                button.trigger()

    def on_mouse_motion(self, x: int, y: int) -> None:
        pass

    def draw(self) -> None:
        for button in self._buttons:
            button.draw()
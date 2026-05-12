from cell import MazeCell
from mazegenerator import MazeGenerator
from typing import List
import arcade


TILE_SIZE: int = 50
SCREEN_WIDTH: int = 850
SCREEN_HEIGHT: int = 850
MOVEMENT_SPEED: int = 2.5


generator = MazeGenerator(size=(15, 15), perfect=False)

MAZE_W: int = len(generator.maze[0])
MAZE_H: int = len(generator.maze)

OFFSET_X: int = (SCREEN_WIDTH - MAZE_W * TILE_SIZE) // 2
OFFSET_Y: int = (SCREEN_HEIGHT - MAZE_H * TILE_SIZE) // 2

maze: List[List[MazeCell]] = [[MazeCell(x, y, col, (MAZE_W, MAZE_H), False)
                              for x, col in enumerate(row)]
                              for y, row in enumerate(generator.maze)]

for row in maze:
    for cell in row:
        cell.center = (
            OFFSET_X + cell.x * TILE_SIZE + TILE_SIZE // 2,
            OFFSET_Y + (MAZE_H - 1 - cell.y) * TILE_SIZE + TILE_SIZE // 2)


class Player:
    def __init__(self, start_x: float, start_y: float) -> None:
        self.sprite = arcade.load_animated_gif("pacman.gif")
        self.sprite.scale = 0.1
        self.sprite.center_x = start_x
        self.sprite.center_y = start_y

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self._sprite_list = arcade.SpriteList()
        self._sprite_list.append(self.sprite)

        self.direction: str = None
        self.next_direction: str = None

    def update(self, delta_time: float) -> None:
        self._sprite_list.update_animation(delta_time)

        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def draw(self) -> None:
        self._sprite_list.draw()


class Level(arcade.View):
    def __init__(self, maze: List[List[MazeCell]]) -> None:
        super().__init__()
        self.maze = maze

        center_x = OFFSET_X + MAZE_W * TILE_SIZE // 2
        center_y = OFFSET_Y + MAZE_H * TILE_SIZE // 2
        self.player = Player(center_x, center_y)

    def on_update(self, delta_time: float) -> None:
        self.player.update(delta_time)

        for row in self.maze:
            for cell in row:
                if cell.center == (int(self.player.sprite.center_x),
                   int(self.player.sprite.center_y)):
                    self.player.change_x = 0
                    self.player.change_y = 0
                    if (self.player.next_direction == "UP"
                        and not cell.walls & 0b0001):
                        self.player.next_direction = None
                        self.player.change_y = MOVEMENT_SPEED
                    elif (self.player.next_direction == "DOWN"
                          and not cell.walls & 0b0100):
                        self.player.next_direction = None
                        self.player.change_y = -MOVEMENT_SPEED
                    elif (self.player.next_direction == "RIGHT"
                          and not cell.walls & 0b0010):
                        self.player.next_direction = None
                        self.player.change_x = MOVEMENT_SPEED
                    elif (self.player.next_direction == "LEFT"
                          and not cell.walls & 0b1000):
                        self.player.next_direction = None
                        self.player.change_x = -MOVEMENT_SPEED
                    else:
                        self.player.next_direction = None
                        self.player.change_x = 0
                        self.player.change_y = 0

    def on_draw(self) -> None:
        self.window.clear()
        self._draw_maze()
        self.player.draw()

    def _draw_maze(self) -> None:
        for row in self.maze:
            for cell in row:
                sx = cell.x * TILE_SIZE + OFFSET_X
                sy = (MAZE_H - 1 - cell.y) * TILE_SIZE + OFFSET_Y

                bl = (sx, sy)
                br = (sx + TILE_SIZE, sy)
                tl = (sx, sy + TILE_SIZE)
                tr = (sx + TILE_SIZE, sy + TILE_SIZE)

                if cell.walls & 0b0001:
                    arcade.draw_line(*tl, *tr, arcade.color.BLUE, 2)
                if cell.walls & 0b0010:
                    arcade.draw_line(*tr, *br, arcade.color.BLUE, 2)
                if cell.walls & 0b0100:
                    arcade.draw_line(*bl, *br, arcade.color.BLUE, 2)
                if cell.walls & 0b1000:
                    arcade.draw_line(*tl, *bl, arcade.color.BLUE, 2)

                arcade.draw_circle_filled(
                    sx + TILE_SIZE // 2,
                    sy + TILE_SIZE // 2,
                    3, arcade.color.WHITE
                )

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self.player.next_direction = "UP"
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.next_direction = "DOWN"
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.next_direction = "LEFT"
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.next_direction = "RIGHT"


def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pac-Man")
    window.show_view(Level(maze))
    arcade.run()


if __name__ == "__main__":
    main()

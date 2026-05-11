from cell import MazeCell
import arcade
from typing import List

from mazegenerator import MazeGenerator


TILE_SIZE: int = 50
MAZE_W, MAZE_H = 19, 19
SCREEN_WIDTH:  int = 1200
SCREEN_HEIGHT: int = 1200
MOVEMENT_SPEED: int = 5

OFFSET_X: int = (SCREEN_WIDTH - MAZE_W * TILE_SIZE) // 2
OFFSET_Y: int = (SCREEN_HEIGHT - MAZE_H * TILE_SIZE) // 2

maze_generator = MazeGenerator(size=(MAZE_W, MAZE_H), perfect=False)
MAZE_W = len(maze_generator.maze[0])
MAZE_H = len(maze_generator.maze)

maze: list[list[MazeCell]] = []
for (y, row) in enumerate(maze_generator.maze):
    maze.append([])
    for (x, col) in enumerate(row):
        maze[y].append(MazeCell(x, y, col, (MAZE_W, MAZE_H), False))


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.sprite_list = arcade.SpriteList()

        self.pacman = arcade.load_animated_gif("pacman.gif")
        self.pacman.scale = 0.1
        self.pacman.center_x = (OFFSET_X + (MAZE_W * TILE_SIZE) / 2 -
                                (TILE_SIZE / 2 if MAZE_W % 2 == 0 else 0))
        self.pacman.center_y = (OFFSET_Y + (MAZE_H * TILE_SIZE) / 2 -
                                (TILE_SIZE / 2 if MAZE_H % 2 == 0 else 0))
        self.sprite_list.append(self.pacman)

    def update(self, delta_time):
        self.sprite_list.update_animation(delta_time)
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self):
        self.sprite_list.draw()


class Level(arcade.View):
    def __init__(self, maze: List[List['MazeCell']]):
        super().__init__()
        self.maze = maze
        self.player = Player()

    def on_update(self, delta_time: float):
        self.player.update(delta_time)

    def on_draw(self) -> None:
        self.window.clear()
        maze_height = len(self.maze)

        for row in self.maze:
            for cell in row:
                screen_x = cell.x * TILE_SIZE + OFFSET_X
                screen_y = (maze_height - 1 - cell.y) * TILE_SIZE + OFFSET_Y

                bottom_left = (screen_x, screen_y)
                bottom_right = (screen_x + TILE_SIZE, screen_y)
                top_left = (screen_x, screen_y + TILE_SIZE)
                top_right = (screen_x + TILE_SIZE, screen_y + TILE_SIZE)

                cell.center = ((screen_x + (TILE_SIZE // 2)),
                               (screen_y + (TILE_SIZE // 2)))
                if cell.walls & 0b0001:
                    arcade.draw_line(*top_left, *top_right,
                                     arcade.color.BLUE, 2)
                if cell.walls & 0b0010:
                    arcade.draw_line(*top_right, *bottom_right,
                                     arcade.color.BLUE, 2)
                if cell.walls & 0b0100:
                    arcade.draw_line(*bottom_left, *bottom_right,
                                     arcade.color.BLUE, 2)
                if cell.walls & 0b1000:
                    arcade.draw_line(*top_left, *bottom_left,
                                     arcade.color.BLUE, 2)
                arcade.draw_circle_filled((screen_x + (TILE_SIZE // 2)),
                                          (screen_y + (TILE_SIZE // 2)),
                                          0.5, arcade.color.RED)
        self.player.draw()

    def on_key_press(self, key):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main() -> None:
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pac-Man")
    game_view = Level(maze)
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()

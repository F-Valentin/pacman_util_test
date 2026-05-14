import arcade

from cell import Cell
from mazegenerator import MazeGenerator
from player import PACMANPlayer
from game_seting import GameSettings
from maze import MazeRenderer


class TestLevel(arcade.View):
    def __init__(self, maze: list[list[Cell]], settings: GameSettings,
                 ) -> None:

        super().__init__()
        self.maze = maze
        self.settings = settings
        self._time_accumulator: float = 0.0

        tile_size = settings.tile_size
        self.maze_w: int = len(maze[0])
        self.maze_h: int = len(maze)
        self.offset_x: int = (
            (settings.screen_width - self.maze_w * tile_size) // 2
        )
        self.offset_y: int = (
            (settings.screen_height - self.maze_h * tile_size) // 2
        )

        self._setup_cells()
        self.renderer = MazeRenderer(
            maze, settings, self.offset_x, self.offset_y, self.maze_h
        )
        self.player = PACMANPlayer(
            *self._compute_player_start(), settings
        )

    def _compute_player_start(self) -> tuple[int, int]:
        tile_size = self.settings.tile_size
        half = self.maze_w * tile_size // 2
        offset = 0 if self.settings.maze_size % 2 != 0 else -tile_size // 2
        return (
            self.offset_x + half + offset,
            self.offset_y + half + offset,
        )

    def _setup_cells(self) -> None:
        tile_size = self.settings.tile_size
        for row in self.maze:
            for cell in row:
                cell.center = (
                    self.offset_x + cell.x * tile_size + tile_size // 2,
                    self.offset_y
                    + (self.maze_h - 1 - cell.y) * tile_size
                    + tile_size // 2,
                )
                cell.has_pacgum = cell.walls != 0x0F

    def on_update(self, delta_time: float) -> None:
        self._time_accumulator += delta_time
        time_step: float = 1 / 60
        while self._time_accumulator >= time_step:
            self._fixed_update(time_step)
            self._time_accumulator -= time_step

    def _fixed_update(self, dt: float) -> None:
        self.player.update(dt)
        player_pixel_x = int(self.player.sprite.center_x)
        player_pixel_y = int(self.player.sprite.center_y)

        for row in self.maze:
            for cell in row:
                if cell.center != (player_pixel_x, player_pixel_y):
                    continue
                self._handle_hub(cell)
                break

    def _handle_hub(self, cell: Cell) -> None:
        cell.has_pacgum = False
        self.player.change_x = 0.0
        self.player.change_y = 0.0
        speed = self.settings.movement_speed
        next_dir = self.player.next_direction

        if next_dir == "UP" and not cell.walls & 0b0001:
            self.player.sprite.angle = -90
            self.player.next_direction = None
            self.player.direction = "UP"
            self.player.change_y = speed
        elif next_dir == "DOWN" and not cell.walls & 0b0100:
            self.player.sprite.angle = 90
            self.player.next_direction = None
            self.player.direction = "DOWN"
            self.player.change_y = -speed
        elif next_dir == "RIGHT" and not cell.walls & 0b0010:
            self.player.sprite.angle = 0
            self.player.next_direction = None
            self.player.direction = "RIGHT"
            self.player.change_x = speed
        elif next_dir == "LEFT" and not cell.walls & 0b1000:
            self.player.sprite.angle = 180
            self.player.next_direction = None
            self.player.direction = "LEFT"
            self.player.change_x = -speed
        else:
            self.player.next_direction = self.player.direction

    def on_draw(self) -> None:
        self.window.clear()
        self.renderer.draw_walls()
        self.renderer.draw_pacgums()
        self.player.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key in (arcade.key.UP, arcade.key.W):
            self.player.next_direction = "UP"
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.next_direction = "DOWN"
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.next_direction = "LEFT"
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.next_direction = "RIGHT"


settings = GameSettings()
generator = MazeGenerator(
    size=(settings.maze_size, settings.maze_size),
    perfect=False,
)
maze_w = len(generator.maze[0])
maze_h = len(generator.maze)
maze: list[list[Cell]] = [
    [
        Cell(x, y, col, (maze_w, maze_h), False)
        for x, col in enumerate(row)
    ]
    for y, row in enumerate(generator.maze)
]
window = arcade.Window(
    settings.screen_width,
    settings.screen_height,
    "Pac-Man",
)
window.show_view(TestLevel(maze, settings))
arcade.run()

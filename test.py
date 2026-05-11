"""Pac-Man — affichage du labyrinthe + déplacement du joueur."""
from cell import MazeCell
from mazegenerator import MazeGenerator
from typing import List
import arcade


# ── Constantes ────────────────────────────────────────────────────────────────

TILE_SIZE: int = 53
SCREEN_WIDTH: int = 850 
SCREEN_HEIGHT: int = 850
MOVEMENT_SPEED: int = 2.5


# ── Génération du labyrinthe ──────────────────────────────────────────────────

_generator = MazeGenerator(size=(15, 15), perfect=False)

MAZE_W: int = len(_generator.maze[0])
MAZE_H: int = len(_generator.maze)

OFFSET_X: int = (SCREEN_WIDTH - MAZE_W * TILE_SIZE) // 2
OFFSET_Y: int = (SCREEN_HEIGHT - MAZE_H * TILE_SIZE) // 2

maze: List[List[MazeCell]] = [
    [MazeCell(x, y, col, (MAZE_W, MAZE_H), False)
     for x, col in enumerate(row)]
    for y, row in enumerate(_generator.maze)
]


# ── Joueur ────────────────────────────────────────────────────────────────────

class Player:
    """Sprite Pac-Man : animation et déplacement pixel par pixel."""

    def __init__(self, start_x: float, start_y: float) -> None:
        self.sprite = arcade.load_animated_gif("pacman.gif")
        self.sprite.scale = 0.1
        self.sprite.center_x = start_x
        self.sprite.center_y = start_y

        self.change_x: float = 0.0
        self.change_y: float = 0.0

        self._sprite_list = arcade.SpriteList()
        self._sprite_list.append(self.sprite)

    def update(self, delta_time: float) -> None:
        self._sprite_list.update_animation(delta_time)
        self.sprite.center_x += self.change_x
        self.sprite.center_y += self.change_y

    def draw(self) -> None:
        self._sprite_list.draw()


# ── Vue principale ────────────────────────────────────────────────────────────

class Level(arcade.View):
    """Vue de jeu : rendu du labyrinthe et gestion des entrées clavier."""

    def __init__(self, maze: List[List[MazeCell]]) -> None:
        """Initialise la vue avec le labyrinthe et crée le joueur au centre.

        Args:
            maze: grille de MazeCell générée.
        """
        super().__init__()
        self.maze = maze

        # centre du labyrinthe en pixels
        center_x = OFFSET_X + MAZE_W * TILE_SIZE / 2
        center_y = OFFSET_Y + MAZE_H * TILE_SIZE / 2
        self.player = Player(center_x, center_y)

    # ── Boucle de jeu ─────────────────────────────────────────────────────────

    def on_update(self, delta_time: float) -> None:
        """Met à jour la logique de jeu chaque frame.

        Args:
            delta_time: temps écoulé depuis la dernière frame (secondes).
        """
        self.player.update(delta_time)

    def on_draw(self) -> None:
        """Dessine la scène complète."""
        self.window.clear()
        self._draw_maze()
        self.player.draw()

    # ── Rendu du labyrinthe ───────────────────────────────────────────────────

    def _draw_maze(self) -> None:
        """Parcourt la grille et dessine les murs de chaque cellule."""
        for row in self.maze:
            for cell in row:
                sx = cell.x * TILE_SIZE + OFFSET_X
                sy = (MAZE_H - 1 - cell.y) * TILE_SIZE + OFFSET_Y

                bl = (sx,             sy)
                br = (sx + TILE_SIZE, sy)
                tl = (sx,             sy + TILE_SIZE)
                tr = (sx + TILE_SIZE, sy + TILE_SIZE)

                cell.center = (sx + TILE_SIZE // 2, sy + TILE_SIZE // 2)

                if cell.walls & 0b0001:  # haut
                    arcade.draw_line(*tl, *tr, arcade.color.BLUE, 2)
                if cell.walls & 0b0010:  # droite
                    arcade.draw_line(*tr, *br, arcade.color.BLUE, 2)
                if cell.walls & 0b0100:  # bas
                    arcade.draw_line(*bl, *br, arcade.color.BLUE, 2)
                if cell.walls & 0b1000:  # gauche
                    arcade.draw_line(*tl, *bl, arcade.color.BLUE, 2)

                arcade.draw_circle_filled(
                    sx + TILE_SIZE // 2,
                    sy + TILE_SIZE // 2,
                    0.5, arcade.color.RED
                )

    # ── Entrées clavier ───────────────────────────────────────────────────────

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Démarre le déplacement du joueur dans la direction pressée.

        Args:
            key: touche enfoncée.
            modifiers: modificateurs actifs (shift, ctrl…).
        """
        if key in (arcade.key.UP, arcade.key.W):
            self.player.change_y = MOVEMENT_SPEED
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.player.change_y = -MOVEMENT_SPEED
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.player.change_x = -MOVEMENT_SPEED
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Arrête le déplacement quand la touche est relâchée.

        Args:
            key: touche relâchée.
            modifiers: modificateurs actifs (shift, ctrl…).
        """
        if key in (arcade.key.UP, arcade.key.DOWN, arcade.key.W, arcade.key.S):
            self.player.change_y = 0.0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT, arcade.key.A, arcade.key.D):
            self.player.change_x = 0.0


# ── Point d'entrée ────────────────────────────────────────────────────────────

def main() -> None:
    """Crée la fenêtre et lance la boucle de jeu."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Pac-Man")
    window.show_view(Level(maze))
    arcade.run()


if __name__ == "__main__":
    main()

import arcade

from game.game_configuration import GameConfig
from level.level import LevelFactory, LevelManager
from player.player import Player
from view_manager import ViewManager
from game.game_state import GameState


class WinView(arcade.View):
    def on_draw(self):
        """ Draw this view """
        self.clear()
        win_text = arcade.Text("Win Screen", self.window.width / 2,
                               self.window.height / 2 + 100,
                               arcade.color.WHITE, font_size=20,
                               anchor_x="center")
        win_text.draw()


class StartView(arcade.View):
    def __init__(self, window: arcade.Window, game_conifg: GameConfig):
        super().__init__()
        self._window = window
        self._game_config = game_conifg

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            GameView(self._window, self._game_config, self)

    def on_draw(self) -> bool | None:
        self.clear()

        start_view = arcade.Text("Press start", self.window.width / 2,
                                 self.window.height / 2,
                                 arcade.color.WHITE, font_size=50,
                                 anchor_x="center")
        start_view.draw()


class GameView(arcade.View):
    def __init__(self, window: arcade.Window, game_config: GameConfig,
                 start_view: StartView):
        super().__init__()
        view_manager = ViewManager(window)
        view_manager.add_view("win_view", WinView())
        view_manager.add_view("game_over", GameOverView(start_view))
        game_state = GameState(view_manager)
        level_manager = LevelManager(window)
        player = Player(game_config.lives)
        level_factory = LevelFactory(
            player=player,
            game_config=game_config,
            maze_size=(10, 10),
            level_switcher=level_manager)
        player.add_death_subscriber(game_state)
        level_manager.add_subscriber(game_state)
        level1 = level_factory.create_level()
        # level2 = level_factory.create_level()
        # level_manager.append_levels([level1, level2])
        level_manager.append_level(level1)
        window.show_view(level1)


class GameOverView(arcade.View):
    def __init__(self, start_view: StartView):
        super().__init__()
        self._start_view = start_view

    def on_draw(self) -> bool | None:
        game_over_text = arcade.Text("Game Over Screen", self.window.width / 2,
                                     self.window.height / 2 + 100,
                                     arcade.color.WHITE, font_size=20,
                                     anchor_x="center")
        game_over_text.draw()

        msg = arcade.Text("Press space to go to the meny",
                          self.window.width / 2,
                          self.window.height / 2 - 100, arcade.color.WHITE,
                          font_size=30, anchor_x="center")

        msg.draw() 

    def on_key_press(self, symbol: int, modifiers: int) -> bool | None:
        if symbol == arcade.key.SPACE:
            self.window.show_view(self._start_view)

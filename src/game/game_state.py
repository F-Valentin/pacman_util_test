from view_manager import ViewManager


class GameState:
    def __init__(self, view_manager: ViewManager):
        self._view_manager = view_manager

    def on_all_levels_completed(self) -> None:
        # TODO
        #self._view_manager.switch_view("win_view")
        pass

    def on_player_death(self) -> None:
        # TODO
        # self._view_manager.switch_view("game_ovvr")
        pass

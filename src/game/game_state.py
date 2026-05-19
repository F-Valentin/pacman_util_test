from view_manager import ViewManager

class GameState:
    def __init__(self, view_manager: ViewManager):
        self._view_manager = view_manager

    def on_all_levels_completed(self) -> None:
        self._view_manager.switch_view("win_view")
  
    def on_player_death(self) -> None:
        self._view_manager.switch_view("game_over")

import arcade
import logging


class ViewManager:
    def __init__(self, window: arcade.Window) -> None:
        self._window = window
        self._views: dict[str, arcade.View] = {}

    def add_view(self, view_name: str, view: arcade.View):
        self._views[view_name] = view

    def switch_view(self, view_name: str) -> bool:
        try:
            view = self._views[view_name]
        except KeyError as e:
            logging.warning(e)
            return False

        self._window.show_view(view)
        return True

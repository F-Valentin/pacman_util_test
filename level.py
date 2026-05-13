import arcade

from abc import ABC, abstractmethod
from mazegenerator import MazeGenerator
from player import Player
from enemy import Ghost
from maze import Maze
from cell import Cell

class LevelSwitcher(ABC):
    @abstractmethod
    def next_level(self):
        pass

class Level(arcade.View):
    def __init__(self, player: Player, ghosts: list[Ghost], maze: Maze, level_switcher: LevelSwitcher) -> None:
        self._player = player
        self._ghosts = ghosts
        self._maze = maze
        self._level_switcher = level_switcher

class LevelFactory:
    def __init__(self) -> None:
        pass

class LevelManager(LevelSwitcher):
    def __init__(self, window: arcade.Window, levels: list[Level]) -> None:
        self._window = window
        self._levels = levels
        self._current = 0
    
    def next_level(self):
        self._current += 1
        self._window.show_view(self._levels[self._current])
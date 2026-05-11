from enum import IntEnum
import arcade

from abc import ABC, abstractmethod
from mazegenerator import MazeGenerator
from player import Player
from enemy import Ghost
from maze import Maze
from cell import Cell

class LevelDifficulty(IntEnum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

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

# simple idea (not finished)
class LevelFactory:
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_level(level_size: tuple[int, int], level_difficulty: LevelDifficulty) -> Level:
        player = Player()
        ghosts = []
        maze_generator = MazeGenerator()
        maze: list[list[Cell]] = []

        for (y, row) in enumerate(maze_generator.maze):
            maze.append([])
            for (x, col) in enumerate(row):
                maze[y].append(Cell(x, y, col, (15, 15), False))
        ...
    
    @staticmethod
    def create_levels(nb_of_levels: int, levels_size: list[tuple[int, int]], levels_difficulty: list[LevelDifficulty]):
        levels: list[Level] = []
        for i in range(nb_of_levels):
            levels.append(LevelFactory.create_level(levels_size[i], levels_difficulty[i]))
        ...

class LevelManager(LevelSwitcher):
    def __init__(self, window: arcade.Window, levels: list[Level]) -> None:
        self._window = window
        self._levels = levels
        self._current = 0
    
    def next_level(self):
        self._current += 1
        self._window.show_view(self._levels[self._current])
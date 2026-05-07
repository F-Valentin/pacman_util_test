# from math_game_utils import Vec2

# t = Vec2(100.0, 200.0)
# t2 = Vec2(100.0, 200.0)

# t3 = t / 2.0

# print(t3)

from mazegenerator import MazeGenerator
from cell import Cell


maze_generator = MazeGenerator(perfect=True)
t = []

maze: list[list[Cell]] = []
for (y, row) in enumerate(maze_generator.maze):
    maze.append([])
    for (x, col) in enumerate(row):
        maze[y].append(Cell(x, y, col, (15, 15), False, False))

for row in maze:
    for col in row:
        print(col)
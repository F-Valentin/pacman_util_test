class Cell:
    """Cellule class used to create better coordinate system."""

    def __init__(self, x: int, y: int, walls: int, size: tuple[int, int],
                 has_visited: bool, ft_pattern: bool):
        self.x: int = x
        self.y: int = y
        self.size: tuple[int, int] = size
        self.walls: int = walls
        self.has_visited: bool = has_visited
        self.neighbors: list[tuple[int, int]] = [
            (x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        self.ft_pattern: bool = ft_pattern

    def __str__(self) -> str:
        return f"cell pos: ({self.x}, {self.y})"
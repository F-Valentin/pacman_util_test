from dataclasses import dataclass


@dataclass
class Rect:
    """Simple rectangle helper used by button hit-testing."""
    x: float
    y: float
    width: float
    height: float
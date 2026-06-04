import arcade
from dataclasses import dataclass


@dataclass
class ScoreUi:
    """Store the score text position and displayed score widget."""
    position: arcade.Vec2
    score_text: arcade.Text

import arcade
from dataclasses import dataclass


@dataclass
class ScoreUi:
    position: arcade.Vec2
    score_text: arcade.Text

from enum import Enum
from random import choice


class Move(Enum):
    LEFT = -1, 0
    RIGHT = 1, 0
    DOWN = 0, -1
    UP = 0, 1
    NONE = 0, 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return {
            Move.LEFT: "🡸",
            Move.RIGHT: "🡺",
            Move.DOWN: "🡻",
            Move.UP: "🡹",
            Move.NONE: "_"
        }[self]

    @staticmethod
    def random():
        return choice([Move.LEFT, Move.RIGHT, Move.UP, Move.DOWN])
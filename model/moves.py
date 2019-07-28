from enum import Enum


class Move(Enum):
    LEFT = -1, 0
    RIGHT = 1, 0
    DOWN = 0, -1
    UP = 0, 1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.move = x, y

    def __str__(self):
        return {
            Move.LEFT: "🡸",
            Move.RIGHT: "🡺",
            Move.DOWN: "🡻",
            Move.UP: "🡹"
        }[self]

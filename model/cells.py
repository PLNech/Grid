from enum import Enum


class Cells(Enum):
    WALL_H = -1
    WALL = 0
    EMPTY = 1
    FOOD = 2
    PLAYER = 3
    CRUMBS = 4

    def __str__(self):
        return {
            self.WALL_H: "|",
            self.WALL: "-",
            self.EMPTY: " ",
            self.FOOD: "⋄",
            self.CRUMBS: "·",
        }[self]

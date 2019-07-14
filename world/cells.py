from enum import Enum


class Cells(Enum):
    WALL = 0
    EMPTY = 1
    FOOD = 2
    PLAYER = 3
    CRUMBS = 4

    def __str__(self):
        return {
            self.WALL: "w",
            self.EMPTY: ".",
            self.FOOD: "X",
            self.PLAYER: "P",
            self.CRUMBS: ",",
        }[self]
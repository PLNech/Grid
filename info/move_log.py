from typing import List

from model.moves import Move


class MoveLog(object):
    moves = ...  # type: List[Move]

    def __init__(self):
        self.moves = []

    def append(self, move):
        self.moves.append(move)

    def __str__(self):
        moves_str = [str(m) for m in self.moves[-20:]]
        return " ".join(moves_str)

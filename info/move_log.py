from typing import List

from model.moves import Move


class MoveLog(object):
    moves = ...  # type: List[Move]

    def __init__(self):
        self.moves = []

    def append(self, move):
        self.moves.append(move)

    def __repr__(self):
        moves_str = [repr(m) for m in self.moves[-3:]]
        return "".join(moves_str)

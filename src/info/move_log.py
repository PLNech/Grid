from typing import List

from model import Move


class MoveLog(object):
    moves = ...  # type: List[Move]

    @property
    def last(self):
        return str(self.moves[-1])

    def __init__(self, limit=30):
        self.moves = []
        self.limit = limit

    def append(self, move):
        self.moves.append(move)

    def __getitem__(self, item):
        return self.moves.__getitem__(item)

    def __len__(self):
        return len(self.moves)

    def __str__(self):
        moves_str = [str(m) for m in self.moves[-self.limit:]]
        return " ".join(moves_str)

from agents import Wanderer
from model import Move

# FIXME: Can't use these due to length difference:
#  see len(glyph.encode('utf-16-le')) // 2
FISH_FULL = "🐡"
FISH = "🐠"


class Lazy(Wanderer):

    def __init__(self, name="Lazy", glyph=None, threshold=10):
        super().__init__(name)
        if glyph is not None:
            self.glyph = glyph
        self.threshold = threshold
        self.resources = threshold + 5

    def choose_move(self, grid):
        if self.has_enough_food:
            return Move.NONE
        else:
            return super().choose_move(grid)

    def choose_to_reproduce(self):
        return self.resources > self.threshold * 2

    @property
    def has_enough_food(self):
        enough = self.resources > self.threshold
        self.name = ("lazy" if enough else "Lazy") + self.name[1]
        self.glyph = self.name[0]
        return enough

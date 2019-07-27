import random
from random import randint

from agents.agent import Agent


class RandomAgent(Agent):
    """
    An agent that acts at random.
    """

    def choose_move(self, grid):
        return self._random_step()

    def _random_step(self):
        if randint(0, 1) == 0:  # Horizontal
            change_x = self.x + random.choice([-1, 1])
            info = "left" if change_x is -1 else "right"
            change_y = self.y
        else:
            change_y = self.y + random.choice([-1, 1])
            info = "down" if change_y is -1 else "up"
            change_x = self.x
        return (change_x, change_y), info
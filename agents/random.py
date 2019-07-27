import random
from random import randint

from agents.agent import Agent


class RandomAgent(Agent):
    """
    An agent that acts at random.
    """

    def act(self, grid):
        info = "score:{:4}".format(self.score)

        # Act
        new_x, new_y = self._random_step()
        was_valid = grid.move_agent(self, new_x, new_y)
        info += "|move(%s)" % self.position
        if not was_valid:
            info += "|invalid"

        reward, new_info = grid.reward_move(new_x, new_y)
        info += new_info

        # We're done if no more resources!
        return reward, grid.stats.resources == 0, info

    def _random_step(self):
        if randint(0, 1) == 0:  # Horizontal
            new_x = self.x + random.choice([-1, 1])
            new_y = self.y
        else:
            new_y = self.y + random.choice([-1, 1])
            new_x = self.x
        return new_x, new_y

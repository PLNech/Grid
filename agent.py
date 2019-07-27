import random
from random import randint

from world.cells import Cells


class Agent(object):

    def __init__(self, name="P"):
        """

        :type name: str
        """
        self.name = name
        self.x = 0
        self.y = 0
        self.score = 0

    def random_step(self):
        if randint(0, 1) == 0:  # Horizontal
            new_x = self.x + random.choice([-1, 1])
            new_y = self.y
        else:
            new_y = self.y + random.choice([-1, 1])
            new_x = self.x
        return new_x, new_y

    def act(self, grid):
        info = "score:{:4}".format(self.score)

        # Act
        new_x, new_y = self.random_step()
        was_valid = grid.move_agent(self, new_x, new_y)
        info += "|move(%s)" % self.position()
        if not was_valid:
            info += "|invalid"

        # Compute reward
        reward = 0
        if grid[self.y][self.x] == Cells.FOOD.value:
            info += "|food"
            reward = 1
            grid[self.y][self.x] = Cells.CRUMBS.value

        # We're done if no more resources!
        return reward, grid.stats.resources == 0, info

    def reward(self, reward):
        """

        :type reward: int
        """
        self.score += reward

    def position(self):
        return "{:2},{:2}".format(self.x, self.y)

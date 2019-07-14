from random import randint

from world.cells import Cells


class Agent(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.score = 0

    def random_step(self):
        if randint(0, 1) == 0:  # Horizontal
            new_x = randint(self.x - 1, self.x + 1)
            new_y = self.y
        else:
            new_y = randint(self.y - 1, self.y + 1)
            new_x = self.x
        return new_x, new_y

    def act(self, grid):
        # Act
        new_x, new_y = self.random_step()
        grid.move_agent(self, new_x, new_y)

        # Compute reward
        reward = 0
        if grid[self.x][self.y] == Cells.FOOD.value:
            reward = 1
            grid[self.x][self.y] = Cells.EMPTY.value
            grid.resources -= 1
            print("Food found! Score: %s, remaining: %s" % (self.score, grid.resources))
        self.score += reward

        # We're done if no more resources!
        return reward, grid.resources == 0

    def random_step(self):
        if randint(0, 1) == 0:  # Horizontal
            new_x = randint(self.x - 1, self.x + 1)
            new_y = self.y
        else:
            new_y = randint(self.y - 1, self.y + 1)
            new_x = self.x
        return new_x, new_y

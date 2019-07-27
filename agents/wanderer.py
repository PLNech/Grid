from IN import INT16_MAX

from agents.agent import Agent
from world.cells import Cells


class Wanderer(Agent):
    def __init__(self, name="W"):
        super().__init__(name)
        self.view = []

    def choose_move(self, grid):
        move = self.x, self.y

        self.view = grid.map
        resources = []
        for y in range(grid.size_y):
            for x in range(grid.size_x):
                if grid[y][x] == Cells.FOOD.value:
                    resources.append((x, y))
        min_distance = INT16_MAX
        for r_x, r_y in resources:
            distance = abs(self.x - r_x) + abs(self.y - r_y)
            if distance < min_distance:
                move = r_x, r_y
        return move, "min(%s)|[see %s]" % (min_distance, len(resources))

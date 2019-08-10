from sys import maxsize

from agents.agent import Agent
from model.cells import Cells


class Wanderer(Agent):
    sight = ...  # type: int

    def __init__(self, name="W", sight=10):
        super().__init__(name)
        self.sight = sight
        self.view = []

    def __str__(self):
        return "[{}|{:02}]".format(self.name, self.sight)

    def choose_move(self, grid):
        self.view = grid.map
        resources, spot_info = self.spot_resources(grid)

        min_distance, nearest = self.analyze_resources(resources)
        if nearest[0] == -1:
            move = self._random_step()
        else:
            move = self.move_towards(nearest)
        return move

    def analyze_resources(self, resources):
        nearest = -1, -1
        min_distance = maxsize

        if len(resources):
            for r_x, r_y in resources:
                distance = abs(self.x - r_x) + abs(self.y - r_y)
                if distance < min_distance:
                    min_distance = distance
                    nearest = r_x, r_y
        return min_distance, nearest

    def spot_resources(self, grid):
        """

        :type grid: Grid
        """
        resources = []
        min_visible_x = -1
        max_visible_x = -1

        min_visible_y = max(0, self.y - self.sight)
        max_visible_y = min(self.y + self.sight, grid.size_y)

        for y in range(min_visible_y, max_visible_y):
            min_visible_x = max(0, self.x - self.sight)
            max_visible_x = min(self.x + self.sight, grid.size_x)

            for x in range(min_visible_x, max_visible_x):
                if grid[y][x] == Cells.FOOD.value:
                    resources.append((x, y))
        return resources, "s[{} {}]/[{} {}]".format(min_visible_x, max_visible_x, min_visible_y, max_visible_y)

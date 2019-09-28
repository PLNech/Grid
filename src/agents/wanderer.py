from sys import maxsize
from typing import List, Tuple

from agents import Agent
from info import Logger


class Wanderer(Agent):
    sight = ...  # type: int

    def __init__(self, name="W", sight=10):
        super().__init__(name)
        self.sight = sight
        self.view = []

    def __str__(self):
        return "[{:3}|{:4}]".format(self.name, self.sight)

    def choose_move(self, grid):
        self.view = grid.map
        resources, spot_info = self.spot_resources(grid)

        min_distance, nearest = self.analyze_resources(resources)
        if nearest[0] == -1:
            move = self._random_move()
        else:
            move = self.move_towards(nearest)
        return move

    def analyze_resources(self, resources):
        nearest = -1, -1
        max_value = 0
        min_distance = maxsize

        if len(resources):
            Logger.get().debug("%i res to analyze." % len(resources))
            for r_x, r_y, value in resources:
                Logger.get().debug("Current best target worth %i." % max_value)
                if max_value <= value:  # Check all resources worth max_value
                    Logger.get().debug("new best resource: %i [%i,%i]" % (value, r_x, r_y))
                    max_value = value
                    distance = abs(self.x - r_x) + abs(self.y - r_y)
                    if distance < min_distance:  # Keep the closest max_value as target
                        Logger.get().debug("new target: %i [%i, %i] (%i)" % (value, r_x, r_y, distance))
                        min_distance = distance
                        nearest = r_x, r_y
        return min_distance, nearest

    def spot_resources(self, grid):
        """

        :type grid: Grid
        :rtype
        """
        resources = []  # type: List[Tuple[int, int, int]]
        min_visible_x = -1
        max_visible_x = -1
        min_visible_y = max(0, self.y - self.sight)
        max_visible_y = min(self.y + self.sight, grid.size_y)

        for y in range(min_visible_y, max_visible_y):
            min_visible_x = max(0, self.x - self.sight)
            max_visible_x = min(self.x + self.sight, grid.size_x)

            for x in range(min_visible_x, max_visible_x):
                value_cell = grid.resources[y][x]  # type: int
                if value_cell > 0:
                    resources.append((x, y, value_cell))
        return resources, "s[{} {}]/[{} {}]".format(min_visible_x, max_visible_x, min_visible_y, max_visible_y)

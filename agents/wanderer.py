from IN import INT16_MAX

from agents.agent import Agent
from world.cells import Cells


class Wanderer(Agent):
    # TODO DEBUG: Spot resources gone wrong :shrug:
    def __init__(self, name="W"):
        super().__init__(name)
        self.view = []

    def choose_move(self, grid):
        self.view = grid.map
        resources, spot_info = self.spot_resources(grid)

        min_distance, nearest = self.analyze_resources(resources)
        if nearest[0] == -1:
            move, choice_info = self._random_step()
        else:
            move, choice_info = self.move_towards(nearest)
        return move, "{:5}|{}|{}|{}".format(choice_info, spot_info, min_distance is not INT16_MAX, len(resources))

    def analyze_resources(self, resources):
        nearest = -1, -1
        min_distance = INT16_MAX

        if len(resources):
            for r_x, r_y in resources:
                distance = abs(self.x - r_x) + abs(self.y - r_y)
                if distance < min_distance:
                    min_distance = distance
                    nearest = r_x, r_y
        else:
            min_distance = INT16_MAX
        return min_distance, nearest

    def spot_resources(self, grid, sight=100):
        """

        :param sight: How far sideways the agent sees resources.

        :type sight int
        :type grid: Grid
        """
        resources = []
        min_visible_x = -1
        max_visible_x = -1

        # Y -> 0 <= self.y - sight TO self.y + sight <= grid.size_y
        min_visible_y = max(0, self.y - sight)
        max_visible_y = min(grid.size_y, self.y + sight)

        for y in range(min_visible_y, max_visible_y):
            # X -> 0 <= self.x - sight TO self.x + sight <= grid.size_x
            min_visible_x = max(0, self.x - sight)
            max_visible_x = min(self.x, self.x + sight)

            for x in range(min_visible_x, max_visible_x):
                if grid[y][x] == Cells.FOOD.value:
                    resources.append((x, y))
        return resources, "s[{} {}]/[{} {}]".format(min_visible_x, max_visible_x, min_visible_y, max_visible_y)

from random import randint

from info.stats import GridStats
from model.cells import Cells


class Grid(object):
    """
    A bidimensional world where agents survive and may thrive.
    """

    def __init__(self, size_x=10, size_y=None, abundance=.1):
        if size_y is None:
            self.size_x, self.size_y = size_x * 2, size_x
        else:
            self.size_x = size_x
            self.size_y = size_y

        self.abundance = abundance
        self.map = []
        self.stats = GridStats(self)

        # Initialize map
        for i in range(self.size_y):
            if i == 0 or i == self.size_y - 1:
                lane = self.wall_lane(self.size_x)
            else:
                lane = self.random_lane(self.size_x)
            self.map.append(lane)

    def __getitem__(self, item):
        return self.map[item]

    # region Grid life
    def is_valid(self, position):
        """
        Returns true if the position is within the map and walkable.

        :type position tuple
        :rtype bool
        """
        x, y = position
        return \
            0 < x < self.size_x - 1 and \
            0 < y < self.size_y - 1 and \
            self.map[y][x] is not Cells.WALL

    # endregion

    # region Map generation
    def random_lane(self, size=10):
        lane = [Cells.WALL_H]

        for i in range(1, size - 1):
            d100 = randint(1, 100)
            if d100 < int(100 * self.abundance):
                cell = Cells.FOOD
            else:
                cell = Cells.EMPTY
            lane.append(cell)
        lane.append(Cells.WALL_H)

        return [cell.value for cell in lane]

    @staticmethod
    def wall_lane(size=10):
        return [Cells.WALL] * size
    # endregion

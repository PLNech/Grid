import random
from math import floor
from random import random
from typing import List

from info import GridStats
from model import Cells


class Grid(object):
    """
    A bidimensional world where agents survive and may thrive.
    """
    resources = ...  # type: List[List[int]]

    def __init__(self, size_x=None, size_y=None, abundance=.0):
        if size_x is None:
            size_x = 20
        self.size_x = size_x
        if size_y is None:
            size_y = floor(size_x * 2)
        self.size_y = size_y

        self.map = []
        self.resources = []
        self.stats = GridStats(self)

        self.init_map(abundance)

    def __getitem__(self, item):
        return self.map[item]

    def init_map(self, abundance):
        for i in range(self.size_y):
            if i == 0 or i == self.size_y - 1:
                lane = Grid.wall_lane(self.size_x)
            else:
                lane = Grid.random_lane(self.size_x, abundance)
            self.map.append(lane)
            self.resources.append([1 if x is Cells.FOOD.value else 0 for x in lane])

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

    def add_resource(self, x, y, value=1):
        self.map[y][x] = Cells.FOOD
        self.resources[y][x] = value
        pass

    def get_resource(self, x, y):
        """ Returns the resources in this cell, leaving crumbs if some food was there."""
        value = self.resources[y][x]
        if value > 0:
            self.map[y][x] = Cells.CRUMBS.value
            self.resources[y][x] = 0
        return value

    def update_resource(self, x, y, value=0):
        """
        Updates the value of the given resource.
        """
        self.resources[y][x] = value

    # endregion

    # region Map generation
    @staticmethod
    def random_lane(size=10, abundance=0):
        lane = [Cells.WALL_H]

        for i in range(1, size - 1):
            if abundance > 0 and random() < abundance:
                cell = Cells.FOOD  # TODO: Replace with plants
            else:
                cell = Cells.EMPTY
            lane.append(cell)
        lane.append(Cells.WALL_H)

        return [cell.value for cell in lane]

    @staticmethod
    def wall_lane(size=10):
        return [Cells.WALL] * size
    # endregion

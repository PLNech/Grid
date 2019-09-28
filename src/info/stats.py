from model import Cells


class GridStats(object):
    def __init__(self, grid):
        """

        :type grid: world.grid.Grid
        """
        self.grid = grid

    def __getattr__(self, item):
        if item is "resources":
            return sum([len([x for x in l if x is Cells.FOOD.value]) for l in self.grid.map])
        elif item is "walls":
            return sum(
                [len([x for x in l if x is Cells.WALL_H or x is Cells.WALL]) for l in self.grid.map])
        else:
            return 0

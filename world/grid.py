from random import randrange, randint

from world.cells import Cells
from world.stats import GridStats


class Grid(object):

    def __init__(self, size=10):
        self.size = size
        self.map = []
        self.agents = []
        self.stats = GridStats(self)

        for i in range(size):
            if i == 0 or i == size - 1:
                lane = self.wall_lane(size)
            else:
                lane = self.random_lane(size)
            self.map.append(lane)

    def __getitem__(self, item):
        return self.map[item]

    def __str__(self):
        grid_str = ""
        for i, lane in enumerate(self.map):
            for j, cell in enumerate(lane):
                cell_str = str(Cells(cell))
                for agent in self.agents:
                    if i == agent.y and j == agent.x:
                        cell_str = agent.name
                grid_str += cell_str
            grid_str += "\n"
        return grid_str

    def move_agent(self, agent, x, y):
        if self.is_valid_move(x, y):
            agent.x, agent.y = x, y
            return True
        return False

    def add_agents(self, agents):
        for a in agents:
            self.add_agent(a)

    def add_agent(self, agent):
        y = randrange(1, self.size - 1)
        x = randrange(1, self.size - 1)

        self.move_agent(agent, x, y)
        self.agents.append(agent)
        return agent

    def is_valid_move(self, x, y):
        return 0 < x < self.size - 1 and \
               0 < y < self.size - 1 and \
               self.map[y][x] is not Cells.WALL

    @staticmethod
    def random_lane(size=10):
        lane = [Cells.WALL_H]

        for i in range(1, size - 1):
            d100 = randint(1, 100)
            if d100 < 10:
                cell = Cells.FOOD
            else:
                cell = Cells.EMPTY
            lane.append(cell)
        lane.append(Cells.WALL_H)

        return [cell.value for cell in lane]

    @staticmethod
    def wall_lane(size=10):
        return [Cells.WALL] * size

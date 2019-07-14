from random import randrange

from world.cells import Cells


class Grid(object):

    def __init__(self, size=10):
        self.size = size
        self.resources = 0
        self.map = []
        self.agents = []

        for i in range(size):
            if i == 0 or i == size - 1:
                lane, resources = self.init_wall(size), 0
            else:
                lane = self.init_lane()
                resources = len([x for x in lane if x is Cells.FOOD.value])
            self.map.append(lane)
            self.resources += resources
        print("Generated map with %s resources." % self.resources)

    def __getitem__(self, item):
        return self.map[item]

    def __str__(self):
        grid_str = ""
        for i, lane in enumerate(self.map):
            for j, cell in enumerate(lane):
                for agent in self.agents:
                    if i == agent.y and j == agent.x:
                        cell_str = str(Cells.PLAYER)
                    else:
                        cell_str = str(Cells(cell))
                    grid_str += cell_str
            grid_str += "\n"
        return grid_str

    def move_agent(self, agent, x, y):
        if self.is_valid_move(x, y):
            agent.x, agent.y = x, y

    def add_agent(self, agent):
        y = randrange(1, self.size - 1)
        x = randrange(1, self.size - 1)

        self.move_agent(agent, x, y)
        self.agents.append(agent)
        return agent

    def is_valid_move(self, x, y):
        return 0 < x < self.size and \
               0 < y < self.size and \
               self.map[y][x] is not Cells.WALL

    @staticmethod
    def init_lane(size=10):
        lane = [0]

        for i in range(1, size - 1):
            cell = randrange(1, len(Cells) - 1)  # TODO: Rarer food
            lane.append(cell)
        lane.append(0)

        return lane

    @staticmethod
    def init_wall(size=10):
        return [0] * size

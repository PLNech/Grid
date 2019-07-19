from random import randrange, randint

from world.cells import Cells


class Grid(object):

    def __init__(self, size=10):
        self.size = size
        self.resources = 0
        self.map = []
        self.agents = []

        for i in range(size):
            if i == 0 or i == size - 1:
                lane, lane_food = self.init_wall(size), 0
            else:
                lane = self.init_lane(size)
                lane_food = len([x for x in lane if x is Cells.FOOD.value])
            self.map.append(lane)
            self.resources += lane_food

    def __getitem__(self, item):
        return self.map[item]

    def __str__(self):
        grid_str = ""
        for i, lane in enumerate(self.map):
            for j, cell in enumerate(lane):
                for agent in self.agents:
                    if i == agent.y and j == agent.x:
                        cell_str = agent.name
                    else:
                        cell_str = str(Cells(cell))
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
    def init_lane(size=10):
        lane = [Cells.WALL]

        for i in range(1, size - 1):
            d100 = randint(1, 100)
            if d100 < 50:
                cell = Cells.FOOD
            else:
                cell = Cells.EMPTY
            lane.append(cell)
        lane.append(Cells.WALL)

        return [cell.value for cell in lane]

    @staticmethod
    def init_wall(size=10):
        return [0] * size

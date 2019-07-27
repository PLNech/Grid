from random import randint, randrange

from world.cells import Cells
from world.stats import GridStats


class Grid(object):
    """
    A bidimensional world where agents survive and may thrive.
    """

    def __init__(self, size_x=10, size_y=None):
        if size_y is None:
            if type(size_x) is tuple:
                self.size_x, self.size_y = size_x
            else:
                self.size_x = size_x
                self.size_y = size_x

        self.size = size_x, size_y
        self.map = []
        self.agents = []
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

    # region Grid life
    def is_valid_move(self, x, y):
        return 0 < x < self.size_x - 1 and \
               0 < y < self.size_y - 1 and \
               self.map[y][x] is not Cells.WALL

    def move_agent(self, agent, x, y):
        """
        Tries to move the agent to the given position.

        :param agent: the agent to move.
        :param x: The desired latitude.
        :param y: The desired longitude.
        :return: True if the agent moved.

        :type agent Agent
        :type x int
        :type y int
        :rtype bool
        """
        if self.is_valid_move(x, y):
            agent.x, agent.y = x, y
            return True
        return False

    def reward_move(self, x, y):
        """
        Rewards the agent for their move.

        :param x: their new longitude.
        :param y: their new latitude.
        :return: the computed reward.

        :type x int
        :type y int
        :rtype int
        """

        info = ""
        reward = 0
        if self[y][x] == Cells.FOOD.value:
            info += "|food"
            reward = 1
            self[y][x] = Cells.CRUMBS.value
        return reward, info

    # endregion

    # region Map generation
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

    def add_agents(self, agents: list):
        """

        :type agents: List[Agent]
        """
        for a in agents:
            self.add_agent(a)

    def add_agent(self, agent):
        y = randrange(1, self.size_y - 1)
        x = randrange(1, self.size_x - 1)

        self.move_agent(agent, x, y)
        self.agents.append(agent)
        return agent
    # endregion

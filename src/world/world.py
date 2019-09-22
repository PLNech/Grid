import string
from random import randrange, randint
from typing import List

from agents import Agent, Sniper
from agents import Wanderer
from model import Cells
from model import Move
from .grid import Grid


class World(object):
    """
    An environment represented by a grid, where agents roam and rules apply.
    """
    agents = ...  # type: List[Agent]

    def __init__(self) -> None:
        self.agents = []
        self.grid = Grid()

    @property
    def alive_agents(self):
        return [a for a in self.agents if a.alive]

    def generate(self, grid_width=20, grid_abundance=.05):
        """
        Generates a new World: a Grid and some Agents.

        :param grid_width: The width of the grid. Height is inferred.
        :param grid_abundance: How abundant resources are.

        :return: the genesis info.
        """
        self.grid = Grid(grid_width, abundance=grid_abundance)

        self.populate()

        return "Generated map of size %s/%s with %s resources and %s walls:\n\n%s" % (
            grid_width, grid_width, self.grid.stats.resources, self.grid.stats.walls, self.print_grid())

    def populate(self):
        self.pop_gleaners(5)
        self.pop_sniper()
        # self.pop_bourgeoisie()

    def pop_bourgeoisie(self):
        self.add_wealthy_wanderer()

    def pop_gleaners(self, nb=5):
        self.add_wanderers(self.grid.size_x, nb)

    def pop_sniper(self, nb=1):
        for a in [Sniper()] * nb:
            self.add_agent(a)

    def add_wealthy_wanderer(self, wealth=1000):
        wealthy = Wanderer()
        wealthy.resources = wealth
        self.add_agent(wealthy)

    def add_wanderers(self, grid_width, nb=5):
        for (i, x) in enumerate(string.ascii_uppercase, 1):
            agent = Wanderer(x, int(i * grid_width / 10))

            self.add_agent(agent)
            if i == nb:
                return

    def add_agents(self, agents: list):
        for a in agents:
            self.add_agent(a)

    def add_agent(self, agent, position=None, near=None):
        """
        Adds this agent at a random place on the map.

        :type near: Agent
        :type agent: Agent
        :type position: tuple
        """

        if near is not None:
            x, y = self.valid_nearby((near.x, near.y))
        elif position is not None:
            x, y = position
        else:
            y = randrange(1, self.grid.size_y - 1)
            x = randrange(1, self.grid.size_x - 1)

        self.put(agent, (x, y))
        self.agents.append(agent)
        return agent

    def move(self, agent, move):
        """
        Tries to move the agent.

        :param agent: the agent to move.
        :param move: The desired move.
        :return: True if the agent moved.

        :type agent Agent
        :type move Move
        :rtype bool
        """
        position = (agent.x + move.x, agent.y + move.y)
        return self.put(agent, position)

    def put(self, agent, position):
        """
        Tries to put the agent at the given position.

        :param agent: the agent to move.
        :param position: The desired position.
        :return: True if the agent moved.

        :type agent Agent
        :type position tuple
        :rtype bool
        """
        if self.grid.is_valid(position):
            agent.x, agent.y = position
            return True
        return False

    def valid_nearby(self, position):
        """
        Returns a walkable cell near the given position.

        :param position: The desired position.

        :type position tuple
        :rtype tuple
        """
        x, y = position

        while not self.grid.is_valid((x, y)):
            x = randint(x - 1, x + 1)
            y = randint(y - 1, y + 1)
        return x, y

    def reward(self, agent):
        """
        Rewards the agent.

        :return: the computed reward.

        :type agent Agent
        :rtype int
        """

        info = "none"
        reward = 0
        x, y = agent.x, agent.y
        if self.grid[y][x] == Cells.FOOD.value:
            info = "food"
            reward = 1
            self.grid[y][x] = Cells.CRUMBS.value
        return reward, info

    def act(self, agent):
        """
        Acts on the given grid, hoping for a reward.

        :param agent: Agent
        :return: reward, done, info.
        """
        info_score = "{:5.1f} res".format(float(agent.resources))
        move = agent.choose_move(self.grid)
        info_log = "{:2}".format(str(agent.move_log))

        was_valid = self.move(agent, move)
        if was_valid:
            info_move = "move"
        else:
            info_move = "fail"
            move = Move.NONE

        agent.move_log.append(move)
        info_move += "(%s)" % agent.position

        reward, info_reward = self.reward(agent)
        if info_reward is None:
            info_reward = "BaseAgent"

        infos = [str(i) for i in [info_score, info_move, info_reward, info_log]]
        info_str = " | ".join(infos)
        return reward, info_str.format(*infos)

        pass

    # TODO: More idiomatic repr with agents
    def print_grid(self):
        grid_str = ""
        for i, lane in enumerate(self.grid.map):
            for j, cell in enumerate(lane):
                cell_str = str(Cells(cell))
                for agent in self.agents:
                    if i == agent.y and j == agent.x:
                        cell_str = agent.glyph
                grid_str += cell_str
            grid_str += "\n"
        return grid_str

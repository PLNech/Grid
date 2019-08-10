from random import randrange
from typing import List

from agents.agent import Agent
from agents.sniper import Sniper
from agents.wanderer import Wanderer
from model.cells import Cells
from world.grid import Grid


class World(object):
    """
    An environment represented by a grid, where agents roam and rules apply.
    """
    agents = ...  # type: List[Agent]

    def __init__(self) -> None:
        self.agents = []
        self.grid = Grid()

    def generate(self, grid_width=20, grid_abundance=.05):
        self.grid = Grid(grid_width, abundance=grid_abundance)

        self.add_agents([Wanderer(x, int(i * grid_width / 10)) for (i, x) in enumerate("ABCDE", 1)])
        self.add_agent(Sniper())

        return "Generated map of size %s, %s with %s resources and %s walls:\n\n%s" % (
            grid_width, grid_width, self.grid.stats.resources, self.grid.stats.walls, self.print_grid())

    def add_agents(self, agents: list):
        for a in agents:
            self.add_agent(a)

    def add_agent(self, agent):
        """
        Adds this agent at a random place on the map.

        :type agent Agent
        """
        y = randrange(1, self.grid.size_y - 1)
        x = randrange(1, self.grid.size_x - 1)

        self.move_agent(agent, (x, y))
        self.agents.append(agent)
        return agent

    def move_agent(self, agent, position):
        """
        Tries to move the agent to the given position.

        :param agent: the agent to move.
        :param position: The desired move.
        :return: True if the agent moved.

        :type agent Agent
        :type position tuple
        :rtype bool
        """
        if self.grid.is_valid(position):
            agent.x, agent.y = position
            return True
        return False

    def reward_move(self, move):
        """
        Rewards the agent for their move.

        :param move: their new position.
        :return: the computed reward.

        :type move tuple
        :rtype int
        """

        info = "none"
        reward = 0
        x, y = move
        if self.grid[y][x] == Cells.FOOD.value:
            info = "food"
            reward = 1
            self.grid[y][x] = Cells.CRUMBS.value
        return reward, info

    # TODO: More idiomatic repr with agents
    def print_grid(self):
        grid_str = ""
        for i, lane in enumerate(self.grid.map):
            for j, cell in enumerate(lane):
                cell_str = str(Cells(cell))
                for agent in self.agents:
                    if i == agent.y and j == agent.x:
                        cell_str = agent.name
                grid_str += cell_str
            grid_str += "\n"
        return grid_str

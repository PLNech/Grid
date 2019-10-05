import string
from random import randrange
from typing import List

from agents import Agent, Sniper
from agents import Wanderer
from agents.plant import Plant
from info import Logger
from model import Cells
from model import Move
from .grid import Grid


class World(object):
    """
    An environment represented by a grid, where agents roam and rules apply.
    """
    agents = ...  # type: List[Agent]
    plants = ...  # type: List[Plant]

    def __init__(self) -> None:
        self.agents = []
        self.plants = []
        self.grid = Grid()

    @property
    def alive_agents(self):
        return [a for a in self.agents if a.alive]

    def generate(self, config):
        """
        Generates a new World: a Grid and some Agents.

        :type config: RunnerConfig
        :param config: Configuration to apply.

        :return: the genesis info.
        """
        self.grid = Grid(config.width, config.height, abundance=config.abundance)

        self.populate(config.scenario)
        self.seed(config.init_plants)

        return "Generated map of size %s/%s with %s resources and %s walls:\n\n%s" % (
            config.height, config.width, self.grid.stats.resources, self.grid.stats.walls, self.print_grid())

    def populate(self, scenario=0):
        if scenario == 0:  # No agents
            return
        elif scenario == 1:  # Lone ranger
            self.pop_gleaners(1)
        elif scenario == 2:  # Classic team
            self.pop_gleaners(5)
            self.pop_sniper()
        elif scenario == 3:  # Let's reproduce
            self.pop_bourgeoisie()

    def pop_bourgeoisie(self):
        self.add_wealthy_wanderer()

    def pop_gleaners(self, nb=5):
        self.add_wanderers(self.grid.size_x, nb)

    def pop_sniper(self, nb=1):
        for a in [Sniper()] * nb:
            self.add_agent(a)

    def seed(self, nb_plants=1):
        for i in range(nb_plants):
            self.add_plant()
        Logger.get().error("%i plants added." % len(self.plants))

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

    def add_agent(self, agent, near=None):
        """
        Adds this agent on the map, near another or randomly.

        :type near: Agent
        :type agent: Agent
        """

        x, y = self.position_entity(near)
        if x != -1:
            self.put(agent, (x, y))
            self.agents.append(agent)
        return agent

    def position_entity(self, near, no_agent=True, no_plant=False):
        if near is not None:
            neighbors = sorted([
                (near.x, near.y + 1),  # Right
                (near.x, near.y - 1),  # Left
                (near.x + 1, near.y),  # Up
                (near.x - 1, near.y)  # .Down
            ])

        for i in range(4):
            # Currently if near=None, we try 4 random positions.
            # TODO: replace random retries with free cell heuristic
            x, y = neighbors[i] if near is not None else \
                (randrange(1, self.grid.size_x - 1),
                 randrange(1, self.grid.size_y - 1))

            is_valid = self.grid.is_valid((x, y))
            is_ok_plant = not (no_plant and self.is_plant(x, y))
            is_ok_agent = not (no_agent and self.is_agent(x, y))
            if is_valid and is_ok_plant and is_ok_agent:
                return x, y
        return -1, -1

    def is_occupied(self, x, y):
        return self.is_agent(x, y), self.is_plant(x, y)

    def is_plant(self, x, y):
        return len([p for p in self.plants if p.x == x and p.y == y]) > 0

    def is_agent(self, x, y):
        return len([a for a in self.agents if a.x == x and a.y == y]) > 0

    def add_plant(self, near=None):
        """
        Adds a plant on the map, near another or randomly.
        :type near: Plant
        :rtype tuple(int, int)
        """
        x, y = self.position_entity(near, no_plant=True)
        if x != -1:
            plant = Plant(x=x, y=y)
            self.plants.append(plant)

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

    def reward(self, agent):
        """
        Rewards the agent.

        :return: the computed reward.

        :type agent Agent
        :rtype int
        """

        x, y = agent.x, agent.y
        reward = self.grid.get_resource(x, y)
        info = "none" if reward is 0 else "food"
        return reward, info

    def act(self, agent):
        """
        Acts on the given grid, hoping for a reward.

        :param agent: Agent
        :return: reward, done, info.
        """
        info_score = "{:3} res".format(agent.resources)
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
    def print_grid(self, show_resources=False):
        grid_str = ""
        content = self.grid.resources if show_resources else self.grid.map

        for i, lane in enumerate(content):
            for j, cell in enumerate(lane):
                cell_str = None

                for plant in self.plants:
                    if i == plant.y and j == plant.x:
                        cell_str = str(plant)
                for agent in self.alive_agents:
                    if i == agent.y and j == agent.x:
                        cell_str = agent.glyph
                if cell_str is None:
                    cell_str = str(cell if show_resources else Cells(cell))
                if cell_str == "0":
                    cell_str = " "

                grid_str += cell_str
            grid_str += "\n"
        return grid_str

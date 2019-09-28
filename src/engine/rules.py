import copy
from math import floor
from random import randint

from agents import Agent
from engine.namer import namer
from info import Logger
from model import Move

VALUE_AGENT_COMPOST = 10


class RuleOutput(object):
    """ Output of a rule: should we stop the run? Anything to show or to log?"""

    def __init__(self, done=False, show=None, log=None):
        self.done = done
        self.show = show
        self.log = log


def make_plants_grow(world):
    """
    Grow plants until they reach their apex size.

    :param world: The world where the rule applies.
    :return: done if done, show for UI and log for logs.

    :rtype tuple(bool, str, str)
    """
    weather = randint(0, 2)  # Either rainy, covered or sunny
    log = ["Rainy", "Covered", "Sunny"][weather] + " day\n"
    log += "%i plants, total biomass %i." % (len(world.plants), sum(p.size for p in world.plants))
    for plant in world.plants:
        log += "\nG{}({:2}, {:2})".format(plant.size, plant.x, plant.y)
        if bool(randint(0, 1)) is True:  # The plant isn't sick or infested
            for i in range(weather):
                plant.grow()
            log += ["", "⇫", "⮸"][weather]
        if plant.size == plant.max_size:  # Reproduction!
            child_x, child_y = world.add_plant(plant)
            log += "-> (%i, %i)" % (child_x, child_y)
            plant.size = 0

    return RuleOutput(False, log, None)


def make_agents_act(world):
    """
    Let each agent make one move.

    :param world: The world where the rule applies.
    :return: done if done, show for UI and log for logs.

    :rtype tuple(bool, str, str)
    """
    show = ""
    log = ""

    for agent in world.alive_agents:
        show += "\n%s " % agent

        reward, info = world.act(agent)
        log = "{}: {} -> {}".format(agent.name, agent.move_log.last, reward)
        agent.process_reward(reward)

        show += "%s |" % agent.position
        if len(info):
            show += info
    return RuleOutput(show=show, log=log)


def make_agents_hungry(world):
    """
    Agents are hungry, losing resources at a random yet regular rate.

    :type world: World
    :rtype: RuleOutput
    """
    for agent in world.alive_agents:  # type: Agent
        # Hungry because the agent just moved, else once in a while
        if len(agent.move_log) and agent.move_log[-1] is Move.NONE or randint(1, 10) == 1:
            agent.resources -= 1
            # Being hungry with an empty stomach doesn't help in this savage grid world
            if agent.resources <= 0:
                agent.alive = False
                world.grid.add_resource(agent.x, agent.y, VALUE_AGENT_COMPOST)
                agent.resources = 0
    return RuleOutput()


def make_agents_reproduce(world):
    """
    Agents can reproduce, making a child if they have enough resources.

    :type world: World
    :rtype: RuleOutput
    """
    for agent in world.alive_agents:  # type: Agent
        if agent.resources > 20:
            if agent.choose_to_reproduce():
                world.add_agent(create_child(agent), near=agent)
    return RuleOutput()


def create_child(agent):
    """

    :type agent: Agent
    :rtype Agent
    """
    clone = copy.copy(agent)  # type: Agent
    clone.resources = floor(agent.resources / 2)
    agent.resources = clone.resources
    clone.glyph, clone.name = namer.name_child(agent.name)
    return clone


def make_last_alive_mohican(world):
    """
    The last agent alive gets 20 resources.

    :type world: World
    :rtype: RuleOutput
    """
    log = ""
    show = ""
    if len(world.alive_agents) == 1:
        last_mohican = world.alive_agents[0]  # type: Agent
        bonus = 20
        last_mohican.resources += bonus
        log = "Last mohican got %i resources (-> %i)!" % (bonus, last_mohican.resources)
        show = "MOHICAN!"

    return RuleOutput(show=show, log=log)


def done_if_nobody_alive(world):
    """
    The world stops if nobody is alive.

    :type world: World
    :rtype: RuleOutput
    """
    return RuleOutput(len(world.alive_agents) == 0)


def done_if_no_resources(world):
    """
    The world stops if it is empty of resources.

    :type world: World
    :rtype: RuleOutput
    """
    return RuleOutput(world.grid.stats.resources == 0)

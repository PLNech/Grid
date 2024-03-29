import copy
from math import floor
from random import randint

from agents import Agent
from engine.namer import namer
from info import Logger, MoveLog
from model import Move

VALUE_AGENT_COMPOST = 10


class RuleOutput(object):
    """ Output of a rule: should we stop the run? Anything to show or to log?"""

    def __init__(self, done=False, show=None, log=None):
        self.done = done
        self.show = show
        self.log = log


# TODO: Indigestion - mort ou lenteur aux bourgeois obèses

def make_plants_grow(world):
    """
    Grow plants until they reach their apex size.

    :param world: The world where the rule applies.
    :return: done if done, show for UI and log for logs.

    :rtype tuple(bool, str, str)
    """
    weather = randint(0, 3)  # Either stormy, rainy, covered or sunny
    log = ["🌩 Storm", "☔ Rain", "⛅ Clouds", "☀  Sunny"][weather] + "\n"
    log += "%i plants, total biomass %i." % (len(world.plants), sum(p.size for p in world.plants))

    for i, plant in enumerate(world.plants):
        Logger.get().error("P:%s" % plant.size)

        if weather == 0:  # Storm!
            if plant.size == 1:  # Shoots don't stand storm
                world.plants.remove(plant)
        if weather > 2:  # Rain
            plant.dry = False
        elif weather == 3:
            if plant.dry and plant.size > 3:  # Dry plants with huge leaves don't stand the sun
                world.plants.remove(plant)
            else:
                plant.dry = True

        if bool(randint(0, 1)) is True:  # The plant isn't sick or infested
            if weather >= 2:  # Sunshine makes a plant grow
                plant.grow(weather)
                world.grid.update_resource(plant.x, plant.y, plant.size)

        if plant.size >= plant.max_size:  # Reproduction!
            world.add_plant(plant)
            world.add_plant(plant)
            plant.size = 0

    # log += "\n%s" % sorted(Counter([p.size for p in world.plants]).items())  # TODO Format stats
    return RuleOutput(False, log)


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


def make_agents_hungry_and_old(world):
    """
    Agents are hungry, losing resources at a random yet regular rate.

    :type world: World
    :rtype: RuleOutput
    """
    for agent in world.alive_agents:  # type: Agent
        agent.age += 1
        # Hungry because the agent just moved, else once in a while
        if len(agent.move_log) and agent.move_log[-1] is Move.NONE or randint(1, 10) == 1:
            agent.resources -= 1
            # Being hungry with an empty stomach doesn't help in this savage grid world
            if agent.resources <= 0:
                agent.alive = False

                # Compost: agent leaves resources, flowers grow
                world.grid.add_resource(agent.x, agent.y, VALUE_AGENT_COMPOST)
                world.add_plants(near=agent)
                agent.resources = 0
    return RuleOutput()


def make_agents_reproduce(world):
    """
    Agents can reproduce, making a child if they have enough resources.

    :type world: World
    :rtype: RuleOutput
    """
    for agent in world.alive_agents:  # type: Agent
        if can_reproduce(agent) and agent.choose_to_reproduce():
            world.add_agent(create_child(agent), near=agent)
    return RuleOutput()


def can_reproduce(agent):
    child_cost = 15
    adult_age = 100
    time_to_recover = 20
    no_child = agent.last_birth == 0

    return agent.resources > child_cost and agent.age > adult_age and no_child or agent.last_birth >= time_to_recover


def create_child(agent):
    """

    :type agent: Agent
    :rtype Agent
    """
    agent.last_birth = 0
    clone = copy.copy(agent)  # type: Agent
    clone.resources = floor(agent.resources / 2)
    agent.resources = clone.resources
    clone.move_log = MoveLog()
    clone.age = 0
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


def done_if_nothing_alive(world):
    """
    The world stops if nothing is alive.

    :type world: World
    :rtype: RuleOutput
    """
    return RuleOutput(len(world.alive_agents) == 0 and len(world.plants) == 0)


def done_if_no_resources(world):
    """
    The world stops if it is empty of resources.

    :type world: World
    :rtype: RuleOutput
    """
    return RuleOutput(world.grid.stats.resources == 0)

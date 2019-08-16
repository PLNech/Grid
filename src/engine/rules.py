import copy
from random import randint

from agents import Agent
from engine.namer import namer

no_show = ""
no_log = ""
default_output = (False, no_show, no_log)


def rule_reproduction(world):
    for agent in world.alive_agents:
        if agent.resources > 20:
            agent.resources = agent.resources / 2

            clone = copy.copy(agent)  # type: Agent
            clone.resources = agent.resources / 2
            clone.glyph, clone.name = namer.name_child(agent.name)
            world.add_agent(clone)

    return default_output


def rule_hunger(world):
    for agent in world.alive_agents:
        if randint(1, 10) == 1:
            agent.resources -= 1
        if agent.resources == 0:
            agent.alive = False
    return len(world.alive_agents) == 0, no_show, no_log


def rule_move_agents(world):
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
    return world.grid.stats.resources == 0, show, log

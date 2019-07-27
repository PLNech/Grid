#! /usr/bin/env python
from curses import wrapper
from typing import List

from agents.agent import Agent
from agents.random import RandomAgent
from agents.wanderer import Wanderer
from world.grid import Grid

grid_height = 10
grid_size = grid_height * 2, grid_height


def main(stdscr):
    stdscr.clear()
    run(stdscr)


def run(window):
    run_i = 0
    done = False
    agents = [RandomAgent(x) for x in "ABCDE"]  # type: List[Agent]
    agents.append(Wanderer())
    grid = Grid(grid_size)
    grid.add_agents(agents)
    window.addstr("Generated map of size %s with %s resources and %s walls:\n\n%s"
                  % (grid_size, grid.stats.resources, grid.stats.walls, grid))
    window.getch()
    window.timeout(50 if sum(grid_size) < 40 else 10)

    while not done:
        window.clear()
        run_i += 1
        window.addstr("Run %s\n" % run_i)
        for agent in agents:
            window.addstr("\n[%s] " % agent.name)

            reward, done, info = agent.act(grid)
            agent.process_reward(reward)
            window.addstr("%s |" % agent.position)
            if len(info):
                window.addstr(info)
        window.addstr("\n\n%s" % grid)
        window.getch()

    window.timeout(10000)
    window.addstr("Done in %i rounds!" % run_i)
    for agent in agents:
        window.addstr("\n%s got %s points."
                      % (agent.name, agent.score))
    window.getch()


if __name__ == "__main__":
    wrapper(main)

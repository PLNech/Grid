#! /usr/bin/env python
from curses import wrapper
from typing import List

from agents.agent import Agent
from agents.wanderer import Wanderer
from world.grid import Grid

grid_height = 20
grid_size = grid_height * 2, grid_height # TODO: Display iso


def main(stdscr):
    while True:
        stdscr.clear()
        run(stdscr)
        stdscr.getch()


def run(window):
    run_i = 0
    done = False
    agents = [Wanderer(x, i * 5) for (i, x) in enumerate("ABCDE", 1)]  # type: List[Agent]
    grid = Grid(grid_size)
    grid.add_agents(agents)
    window.addstr("Generated map of size %s with %s resources and %s walls:\n\n%s"
                  % (grid_size, grid.stats.resources, grid.stats.walls, grid))
    window.timeout(5000)
    window.getch()
    window.timeout(50 if sum(grid_size) < 40 else 10)

    while not done:
        window.clear()
        run_i += 1
        window.addstr("Run %s\n" % run_i)
        for agent in agents:
            window.addstr("\n%s " % agent)

            reward, done, info = agent.act(grid)
            agent.process_reward(reward)
            window.addstr("%s |" % agent.position)
            if len(info):
                window.addstr(info)
        window.addstr("\n\n%s" % grid)
        window.getch()

    window.timeout(10000)
    window.addstr("\nDone in %i rounds!" % run_i)
    agents.sort(key=lambda a: a.score)
    for agent in agents:
        window.addstr("\n%s got %s points."
                      % (agent.name, agent.score))
    window.getch()


if __name__ == "__main__":
    wrapper(main)

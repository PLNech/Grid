#! /usr/bin/env python
from curses import wrapper
from typing import List

from agents.agent import Agent
from agents.random import RandomAgent
from world.grid import Grid

grid_size = 20, 10


def main(stdscr):
    stdscr.clear()
    run(stdscr)


class Wanderer(Agent):
    def __init__(self, name="W"):
        super().__init__(name)
        self.view = []

    def act(self, grid):
        return super().act(grid)

    def process_reward(self, reward):
        super().process_reward(reward)


def run(window):
    run_i = 0
    done = False
    agents = [RandomAgent(x) for x in "ABCDE"]
    # agents.append(Wanderer())
    grid = Grid(grid_size)
    grid.add_agents(agents)
    window.addstr("Generated map of size %s with %s resources and %s walls:\n\n%s"
                  % (grid_size, grid.stats.resources, grid.stats.walls, grid))
    window.getch()
    window.timeout(50 if sum(grid_size) < 40 else 0)

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
    window.addstr("Done!")
    for agent in agents:
        window.addstr("\n%s Got %s points in %s rounds."
                      % (agent.name, agent.score, run_i))
    window.getch()


if __name__ == "__main__":
    wrapper(main)

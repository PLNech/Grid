#! /usr/bin/env python

from curses import wrapper

from agent import Agent
from world.grid import Grid


def main(stdscr):
    stdscr.clear()
    run(stdscr)


def run(stdscr):
    run_i = 0
    done = False
    agents = [Agent("A"), Agent("B")]
    grid = Grid()
    grid.add_agents(agents)
    stdscr.addstr("Generated map with %s resources:\n\n%s"
                  % (grid.resources, grid))
    stdscr.getch()

    while not done:
        stdscr.clear()
        run_i += 1
        stdscr.addstr("Run %s\n" % run_i)
        for a in agents:
            stdscr.addstr("\n[%s] " % a.name)

            reward, done, info = a.act(grid)
            a.reward(reward)
            stdscr.addstr("%s (%s,%s) |" % (reward, a.x, a.y))
            if len(info):
                stdscr.addstr("Info: %s" % info)
        stdscr.addstr("\n\n%s" % grid)
        stdscr.getch()

    stdscr.addstr("Done!")
    for a in agents:
        stdscr.addstr("\n%s Got %s points in %s rounds."
                      % (a.name, a.score, run_i))
    stdscr.getch()


if __name__ == "__main__":
    wrapper(main)

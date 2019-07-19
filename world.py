#! /usr/bin/env python

from curses import wrapper

from agent import Agent
from world.grid import Grid

SIZE = 40


def main(stdscr):
    stdscr.clear()
    run(stdscr)


def run(window):
    run_i = 0
    done = False
    agents = [Agent(x) for x in "ABCDE"]
    grid = Grid(SIZE)
    grid.add_agents(agents)
    window.addstr("Generated map with %s resources:\n\n%s"
                  % (grid.resources, grid))
    window.getch()
    window.timeout(50 if SIZE < 20 else 0)

    while not done:
        window.clear()
        run_i += 1
        window.addstr("Run %s\n" % run_i)
        for a in agents:
            window.addstr("\n[%s] " % a.name)

            reward, done, info = a.act(grid)
            a.reward(reward)
            window.addstr("%s |" % a.position())
            if len(info):
                window.addstr(info)
        window.addstr("\n\n%s" % grid)
        window.getch()

    window.timeout(10000)
    window.addstr("Done!")
    for a in agents:
        window.addstr("\n%s Got %s points in %s rounds."
                      % (a.name, a.score, run_i))
    window.getch()


if __name__ == "__main__":
    wrapper(main)

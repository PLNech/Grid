from curses import wrapper

from agent import Agent
from world.grid import Grid


def main(stdscr):
    stdscr.clear()
    run(stdscr)


def run(stdscr):
    run_i = 0
    done = False
    agent = Agent()
    grid = Grid()
    stdscr.addstr("Generated map with %s resources." % grid.resources)

    grid.add_agent(agent)
    stdscr.addstr(str(grid))

    while not done:
        stdscr.clear()
        run_i += 1
        reward, done = agent.act(grid)
        stdscr.addstr("Run %s: %s\n%s (%s,%s)" % (run_i, reward, grid, agent.x, agent.y))
        stdscr.getch()

    stdscr.addstr("Done! Got %s points in %s rounds." % (agent.score, run_i))
    stdscr.getch()


if __name__ == "__main__":
    wrapper(main)

#! /usr/bin/env python

from curses import wrapper

from world.world import World

grid_abundance = .05
grid_height = 20
grid_size = grid_height * 2, grid_height  # TODO: Display iso
timeout_pauses = 3000
timeout_run = 50 if sum(grid_size) < 40 else 1


def main(stdscr):
    while True:
        # TODO: Loop N times, then stats on agents
        stdscr.clear()
        run(stdscr)
        stdscr.getch()


def run(window):
    run_i = 0
    done = False

    world = World()
    info = world.generate(grid_height, grid_abundance)

    window.addstr(info)
    window.timeout(timeout_pauses)
    window.getch()

    window.timeout(timeout_run)
    while not done:
        run_i += 1
        window.clear()
        window.addstr("Run %s\n" % run_i)
        for agent in world.agents:
            window.addstr("\n%s " % agent)

            reward, done, info = agent.act(world)
            agent.process_reward(reward)
            window.addstr("%s |" % agent.position)
            if len(info):
                window.addstr(info)
        window.addstr("\n\n%s" % world.print_grid())
        window.getch()

    window.timeout(timeout_pauses)
    window.addstr("\nDone in %i rounds!" % run_i)
    world.agents.sort(key=lambda a: a.score)
    for agent in world.agents:
        window.addstr("\n%s got %s points."
                      % (agent.name, agent.score))
    window.getch()


if __name__ == "__main__":
    wrapper(main)

# from run_world import grid_height, grid_abundance, timeout_pauses, timeout_run

from engine.rules import *
from info import Logger
from world import World


class RunnerConfig(object):
    def __init__(self, height=20, abundance=.1, timeout_pauses=1000, timeout_run=0) -> None:
        self.abundance = abundance
        self.height = height
        self.timeout_run = timeout_run
        self.timeout_pauses = timeout_pauses


class Runner(object):
    def __init__(self, stdscr, config=RunnerConfig()) -> None:
        self.config = config
        self.scr = stdscr
        self.log = Logger(stdscr)

    # TODO: Loop N times, then stats on agents
    def run_infinite(self):
        while True:
            self.scr.clear()
            self.run()
            self.scr.getch()

    def run(self):
        world = self.init_world()

        self.run_episode(world)

        format_score = "{:" + str(max([len(str(a.score)) for a in world.agents])) + "}"
        format_fails = "{:" + str(max([len(str(a.fails)) for a in world.agents])) + "}"

        world.agents.sort(key=lambda a: a.resources)
        for agent in world.agents:
            info_score = format_score.format(agent.score)
            info_fails = format_fails.format(agent.fails)

            msg = "\n{:2} got {} points, failed {} times.".format(agent.name, info_score, info_fails)
            self.log.print(msg)
        self.scr.getch()

    def run_episode(self, world):
        run_i = 0
        done = False

        # namer.reset()
        self.scr.timeout(self.config.timeout_run)
        while not done:
            run_i += 1
            done = self.run_round(run_i, world)

        self.scr.timeout(self.config.timeout_pauses)
        self.log.print("\nDone in %i rounds!" % run_i)

    def run_round(self, run_i, world):
        done = False
        rules = [make_agents_hungry,
                 make_agents_reproduce,
                 make_agents_act,
                 make_last_alive_mohican,
                 done_if_nobody_alive,
                 done_if_no_resources]

        self.scr.clear()
        self.log.show("Run %s\n" % run_i)

        for rule in rules:
            output = rule(world)
            done = done or output.done
            self.log.show(output.show)
            self.log.log(output.log)

        self.log.show("\n\n%s" % world.print_grid())
        self.scr.getch()
        return done

    def init_world(self):
        world = World()
        info = world.generate(self.config.height, self.config.abundance)

        self.log.print(info)
        self.scr.timeout(self.config.timeout_pauses)
        self.scr.getch()
        return world

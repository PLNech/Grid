# from run_world import grid_height, grid_abundance, timeout_pauses, timeout_run

from engine.rules import *
from info import Logger
from world import World


class RunnerConfig(object):
    def __init__(self,
                 height=20,
                 width=None,
                 abundance=.1, init_plants=1,
                 timeout_pauses=5000, timeout_run=0,
                 scenario=0) -> None:
        self.abundance = abundance
        self.height = height
        self.width = width
        self.init_plants = init_plants
        self.timeout_run = timeout_run
        self.timeout_pauses = timeout_pauses
        self.scenario = scenario


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

        if len(world.agents):
            format_score = "{:" + str(max([len(str(a.score)) for a in world.agents])) + "}"
            format_fails = "{:" + str(max([len(str(a.fails)) for a in world.agents])) + "}"

        world.agents.sort(key=lambda a: a.score, reverse=True)
        for agent in world.agents:
            info_score = format_score.format(agent.score)
            info_fails = format_fails.format(agent.fails)

            msg = "\n{:4} got {} points, failed {} times.".format(agent.name, info_score, info_fails)
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
        show = ""
        log = ""
        rules = [
            make_plants_grow,
            make_agents_hungry,
            make_agents_reproduce,
            make_agents_act,
            # make_last_alive_mohican,
            done_if_nothing_alive
        ]

        for rule in rules:
            output = rule(world)
            done = done or output.done
            if output.show:
                show += output.show
            if output.log:
                log += output.log

        self.scr.clear()
        self.log.show("Run %s\n\n%s" % (run_i, world.print_grid()))
        self.log.show(show)
        self.scr.getch()

        if len(log):
            self.log.log(log)
        return done

    def init_world(self):
        world = World()
        info = world.generate(self.config)

        self.log.print(info)
        self.scr.timeout(self.config.timeout_pauses)
        self.scr.getch()
        return world

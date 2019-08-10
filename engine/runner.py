# from run_world import grid_height, grid_abundance, timeout_pauses, timeout_run
from random import randint

from world.world import World


class RunnerConfig(object):
    def __init__(self, height=20, abundance=.05, timeout_pauses=1000, timeout_run=0) -> None:
        self.abundance = abundance
        self.height = height
        self.timeout_run = timeout_run
        self.timeout_pauses = timeout_pauses


class Runner(object):

    def __init__(self, stdscr, config=RunnerConfig()) -> None:
        self.config = config
        self.scr = stdscr

    # TODO: Loop N times, then stats on agents
    def run_infinite(self):
        while True:
            self.scr.clear()
            self.run()
            self.scr.getch()

    def run(self):
        world = self.init_world()

        self.run_episode(world)

        len_scores = max([len(str(a.score)) for a in world.agents])
        len_fails = max([len(str(a.fails)) for a in world.agents])
        format_score = "{:" + str(len_scores) + "}"
        format_fails = "{:" + str(len_fails) + "}"

        world.agents.sort(key=lambda a: a.resources)
        for agent in world.agents:
            info_score = format_score.format(agent.score)
            info_fails = format_fails.format(agent.fails)

            self.scr.addstr("\n{} got {} points, failed {} times."
                            .format(agent.name, info_score, info_fails))
        self.scr.getch()

    def run_episode(self, world):
        run_i = 0
        done = False

        self.scr.timeout(self.config.timeout_run)
        while not done:
            run_i += 1
            done = self.run_round(run_i, world)

        self.scr.timeout(self.config.timeout_pauses)
        self.scr.addstr("\nDone in %i rounds!" % run_i)

    def run_round(self, run_i, world):
        done = False

        self.scr.clear()
        self.scr.addstr("Run %s\n" % run_i)

        done = self.rule_move_agents(world)
        done = self.rule_hunger(world)

        self.scr.addstr("\n\n%s" % world.print_grid())
        self.scr.getch()
        return done

    def rule_move_agents(self, world):
        done = False
        for agent in [a for a in world.agents if a.alive]:
            self.scr.addstr("\n%s " % agent)

            reward, done, info = world.act(agent)
            agent.process_reward(reward)

            self.scr.addstr("%s |" % agent.position)
            if len(info):
                self.scr.addstr(info)
        return done

    def rule_hunger(self, world):
        for agent in world.agents:
            d10 = randint(1, 10)
            if d10 == 1:
                agent.resources -= 1
            if agent.resources == 0:
                agent.alive = False
        return len([a for a in world.agents if a.alive]) == 0

    def init_world(self):
        world = World()
        info = world.generate(self.config.height, self.config.abundance)

        self.scr.addstr(info)
        self.scr.timeout(self.config.timeout_pauses)
        self.scr.getch()
        return world

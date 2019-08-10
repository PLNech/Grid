# from run_world import grid_height, grid_abundance, timeout_pauses, timeout_run
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
        run_i = 0
        done = False

        world = World()
        info = world.generate(self.config.height, self.config.abundance)

        self.scr.addstr(info)
        self.scr.timeout(self.config.timeout_pauses)
        self.scr.getch()

        self.scr.timeout(self.config.timeout_run)
        while not done:
            run_i += 1
            self.scr.clear()
            self.scr.addstr("Run %s\n" % run_i)
            for agent in world.agents:
                self.scr.addstr("\n%s " % agent)

                reward, done, info = agent.act(world)
                agent.process_reward(reward)
                self.scr.addstr("%s |" % agent.position)
                if len(info):
                    self.scr.addstr(info)
            self.scr.addstr("\n\n%s" % world.print_grid())
            self.scr.getch()

        self.scr.timeout(self.config.timeout_pauses)
        self.scr.addstr("\nDone in %i rounds!" % run_i)
        world.agents.sort(key=lambda a: a.score)
        for agent in world.agents:
            self.scr.addstr("\n%s got %s points."
                            % (agent.name, agent.score))
        self.scr.getch()

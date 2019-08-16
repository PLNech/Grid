#! /usr/bin/env python

from curses import wrapper

from engine.runner import Runner, RunnerConfig

grid_abundance = .05
grid_height = 20
timeout_pauses = 1000
timeout_run = 50 if grid_height < 20 else 100


def main(stdscr):
    config = RunnerConfig(grid_height, grid_abundance, timeout_pauses, timeout_run)
    runner = Runner(stdscr, config)
    runner.run_infinite()


if __name__ == "__main__":
    wrapper(main)

#! /usr/bin/env python
import argparse
from curses import wrapper

from engine import Runner, RunnerConfig

default_abundance = .05
default_grid_height = 10
default_grid_width = None
default_pauses = 1000
default_timeout = 50 if default_grid_height < 20 else 10
default_plants = 0


def main(stdscr):
    config = RunnerConfig(args.height,
                          args.width,
                          args.abundance,
                          args.plants,
                          args.pause,
                          args.timeout,
                          args.scenario)  # type: RunnerConfig
    runner = Runner(stdscr, config)
    runner.run_infinite()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A grid world where agents thrive and survive.")
    parser.add_argument("-H", "--height", type=int, default=default_grid_height,
                        metavar="21",
                        help="The height of the square grid.")
    parser.add_argument("-W", "--width", type=int, default=default_grid_width,
                        metavar="21",
                        help="The height of the square grid.")
    parser.add_argument("-a", "--abundance", type=float, default=default_abundance,
                        metavar=".1",
                        help="The abundance of resources on the grid.")
    parser.add_argument("-p", "--plants", type=int, default=default_plants,
                        metavar="1",
                        help="How many plants on the initial grid.")
    parser.add_argument("-P", "--pause", type=int, default=default_pauses,
                        metavar="1000",
                        help="Pause in milliseconds at map generation and death.")
    parser.add_argument("-t", "--timeout", type=int, default=default_timeout,
                        metavar="10",
                        help="Pause between each round of actions.")
    parser.add_argument("-s", "--scenario", type=int, default=0,
                        metavar="0",
                        help="Choose a scenario.")
    args = parser.parse_args()
    print(args.height, args.width)
    wrapper(main)

import logging
import os
from datetime import datetime


class Logger(object):

    def __init__(self, stdscr) -> None:
        if not os.path.exists("logs"):
            os.makedirs("logs")

        self.logger = logging.getLogger("grid_world")
        logging.basicConfig(filename=datetime.now().strftime('logs/%Y_%m_%d-%H:%M.log'),
                            filemode="w+",
                            level=logging.DEBUG,
                            format='%(asctime)s,%(msecs)d %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            )
        logging.addLevelName(logging.DEBUG, '[D]')
        logging.addLevelName(logging.INFO, '[I]')
        logging.addLevelName(logging.WARNING, '[W]')
        logging.addLevelName(logging.ERROR, '[E]')
        self.scr = stdscr

    def print(self, msg="", lvl=logging.DEBUG):
        self.show(msg)
        self.log(msg.strip("\n"), lvl)

    def show(self, msg):
        self.scr.addstr(msg)

    def log(self, msg="", lvl=logging.DEBUG):
        logging.log(lvl, msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logging.shutdown()

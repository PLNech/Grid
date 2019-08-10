import random
from abc import abstractmethod

from info.move_log import MoveLog
from model.moves import Move


class Agent(object):
    """
    An autonomous agent acting on a Grid to get rewards.
    """

    def __init__(self, name="P"):
        """
        Initialize the agent's default state, before being anywhere on the Grid.

        :type name: str
        """
        self.name = name
        self.x = 0
        self.y = 0
        self.score = 0
        self.log = MoveLog()

    def __str__(self):
        return "[{}]".format(self.name)

    # region Agent-specific methods
    def process_reward(self, reward):
        """
        Handles reward: maybe learn, at least score that down.

        :type reward int
        """
        self.score += reward

    @abstractmethod
    def choose_move(self, grid):
        return self.x, self.y

    # endregion

    def act(self, world):  # TODO: Invert control, don't let agent touch world
        """
        Acts on the given grid, hoping for a reward.

        :param world: World
        :return: reward, done, info.
        """
        info_score = "score:{:3}".format(self.score)
        move = self.choose_move(world.grid)
        info_log = "{:2}".format(repr(self.log))

        was_valid = world.move_agent(self, move)
        if not was_valid:
            info_move = "|invalid!"
        else:
            self.log.append(move)
            info_move = "|move(%s)" % self.position

        reward, info_reward = world.reward_move(move)
        if info_reward is None:
            info_reward = "BaseAgent"

        infos = [str(i) + "/" for i in [info_score, info_move, info_log, info_reward]]
        info_str = "|".join(["{}" * len(infos)])
        return reward, world.grid.stats.resources == 0, info_str.format(*infos)

    def move_towards(self, position):
        """
        Moves the agent towards the given position.

        :param position: a (x, y) position to reach.
        :return: the move coordinates.
        """
        d_x, d_y = position
        if self.x != d_x:
            move = Move.LEFT if d_x - self.x < 0 else Move.RIGHT
        else:
            move = Move.DOWN if d_y - self.y < 0 else Move.UP
        return self.destination_of(move)

    def destination_of(self, m):
        return self.x + m.x, self.y + m.y

    def _random_step(self):
        move = random.choice(list(Move))
        return self.move_towards(self.destination_of(move))

    @property
    def position(self):
        return "{:02},{:02}".format(self.x, self.y)

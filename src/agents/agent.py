from abc import abstractmethod

from info import MoveLog
from model import Move


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
        self.alive = True
        self.move_log = MoveLog()
        self.resources = 10
        self.score = 0

    @property
    def fails(self):
        return len([x for x in self.move_log.moves if x is Move.NONE])

    def __str__(self):
        return "[{}]".format(self.name)

    # region Agent-specific methods
    def process_reward(self, reward):
        """
        Handles reward: maybe learn, at least score that down.

        :type reward int
        """
        self.resources += reward
        self.score += reward

    @abstractmethod
    def choose_move(self, grid):
        return self.x, self.y

    # endregion

    def move_towards(self, position):
        """
        Moves the agent towards the given position.

        :param position: a (x, y) position to reach.
        :return: the right move.

        :rtype Move
        """
        d_x, d_y = position

        if self.x != d_x:
            return Move.LEFT if d_x - self.x < 0 else Move.RIGHT
        else:
            return Move.DOWN if d_y - self.y < 0 else Move.UP

    def _random_move(self):
        return Move.random()

    @property
    def position(self):
        return "{:02},{:02}".format(self.x, self.y)

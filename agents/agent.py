from abc import abstractmethod
from random import randint, choice


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

    # region Agent-specific methods
    def process_reward(self, reward):
        """
        Handles reward: maybe learn, at least score that down.

        :type reward int
        """
        self.score += reward

    @abstractmethod
    def choose_move(self, grid):
        info = ""
        return (self.x, self.y), info

    # endregion

    def act(self, grid):
        """
        Acts on the given grid, hoping for a reward.

        :param grid: Grid
        :return: (reward, done, info) tuple.
        """
        info = "score:{:4}".format(self.score)
        move, choice_info = self.choose_move(grid)
        info += "|{:25}".format(choice_info)

        was_valid = grid.move_agent(self, move)
        if not was_valid:
            info += "|invalid"
        else:
            info += "|move(%s)" % self.position

        reward, reward_info = grid.reward_move(move)
        if reward_info is None:
            reward_info = "BaseAgent"

        return reward, grid.stats.resources == 0, info + reward_info

    def move_towards(self, destination):
        """
        Moves the agent towards the given destination.

        :param destination: a (x, y) destination to reach.
        :return: the move coordinates and the verbose move taken.
        """
        d_x, d_y = destination
        if self.x != d_x:
            change = -1 if d_x - self.x < 0 else 1
            info = "left" if change is -1 else "right"
            return (self.x + change, self.y), info
        else:
            change = (-1 if d_y - self.y < 0 else 1)
            info = "down" if change is -1 else "up"
            return (self.x, self.y + change), info

    def _random_step(self):
        change = choice([-1, 1])
        if randint(0, 1) == 0:  # Horizontal
            destination = (self.x + change, self.y)
        else:
            destination = (self.x, self.y + change)
        return self.move_towards(destination)

    @property
    def position(self):
        return "{:2},{:2}".format(self.x, self.y)

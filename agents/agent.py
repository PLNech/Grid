from abc import abstractmethod


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
        move, new_info = self.choose_move(grid)

        was_valid = grid.move_agent(self, move)

        info += "|move(%s)|%s" % (self.position, new_info)
        if not was_valid:
            info += "|invalid"

        reward, new_info = grid.reward_move(move)
        if new_info is None:
            new_info = "BaseAgent"
        info += new_info

        return reward, grid.stats.resources == 0, info + new_info

    @property
    def position(self):
        return "{:2},{:2}".format(self.x, self.y)

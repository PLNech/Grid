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

    def act(self, grid):
        """
        Acts on the given grid, hoping for a reward.
        :param grid: Grid

        :return: (reward, done, info) tuple.
        """
        return 0, False, "BASEAgent"

    def process_reward(self, reward):
        """
        Handles reward: maybe learn, at least score that down.

        :type reward: int
        """
        self.score += reward

    @property
    def position(self):
        return "{:2},{:2}".format(self.x, self.y)

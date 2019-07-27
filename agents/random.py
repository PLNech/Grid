from agents.agent import Agent


class RandomWalker(Agent):
    """
    An agent that acts at random.
    """

    def __init__(self, name="R"):
        super().__init__(name)

    def choose_move(self, grid):
        return self._random_step()

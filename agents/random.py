from agents.agent import Agent


class RandomAgent(Agent):
    """
    An agent that acts at random.
    """

    def choose_move(self, grid):
        return self._random_step()

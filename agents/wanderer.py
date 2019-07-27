from agents.agent import Agent


class Wanderer(Agent):
    def __init__(self, name="W"):
        super().__init__(name)
        self.view = []

    def choose_move(self, grid):
        return super().choose_move(grid)



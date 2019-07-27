from agents.wanderer import Wanderer


class Sniper(Wanderer):
    def __init__(self, name="S"):
        super().__init__(name, 1000)

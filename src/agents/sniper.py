from .wanderer import Wanderer


class Sniper(Wanderer):
    def __init__(self, name=None):
        if name is None:
            name = "S"
        super().__init__(name, 1000)

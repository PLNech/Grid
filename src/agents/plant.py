class Plant(object):
    """
    A barely autonomous entity growing on a Grid.
    """

    def __init__(self, max_size=5, x=-1, y=-1):
        self.max_size = max_size
        self.size = 0
        self.x, self.y = x, y

    def grow(self):
        if self.size < self.max_size:
            self.size += 1

    def __str__(self) -> str:
        return [
            "՛",
            "՜",
            "՞",
            "Ր",
            "ր",
            "փ",
            "թ",
            "Ք",
            "ք",
            "Ց"][self.size]

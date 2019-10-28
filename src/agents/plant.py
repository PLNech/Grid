class Plant(object):
    """
    A barely autonomous entity growing on a Grid.
    """

    def __init__(self, max_size=5, x=-1, y=-1):
        self.max_size = max_size
        self.size = 0
        self.dry = False
        self.x, self.y = x, y

    def grow(self, weather):  # weather: 2 (covered) / 3 (sunny)
        if self.size < self.max_size:
            self.size += 1 if self.size < 2 else (weather - 1)

    def __str__(self) -> str:
        return [
            "·",
            "𔗉",
            "𔒱",
            "𔓘",
            "𔒰",
        ][self.size]

    def __repr__(self) -> str:
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
            "Ց"
        ][self.size]

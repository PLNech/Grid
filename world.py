from random import randrange, randint

CELLS = {
    "wall": 0,
    ",": 1,
    "O": 2,
    "P": 3
}


def init_lane(size=10):
    lane = [0]

    for i in range(1, size - 1):
        cell = randrange(1, len(CELLS) - 1)  # TODO: Rarer food
        lane.append(cell)
    lane.append(0)

    return lane


def init_wall(size=10):
    return [0] * size


def init_grid(size=10):
    grid = []

    for i in range(size):
        grid.append(init_wall(size) if i == 0 or i == size - 1 else init_lane())
    return grid


def cell_to_str(cell):
    for name, code in CELLS.items():
        if cell == code:
            return name[0:1]
    return "?"


def print_world(grid, agent):
    world_rep = ""
    for lane in grid:
        world_rep += "%s\n" % "".join([cell_to_str(cell) for cell in lane])
    print(world_rep)


class Agent(object):

    def __init__(self):
        self.x = 0
        self.y = 0
        self.score = 0

    def act(self, grid):
        if randint(0, 1) == 0:  # Horizontal
            new_x = randint(self.x - 1, self.x + 1)
            new_y = self.y
        else:
            new_y = randint(self.y - 1, self.y + 1)
            new_x = self.x

        move_agent(self, grid, new_x, new_y)
        # print("New position: ", self.x, self.y)
        if grid[self.x][self.y] == CELLS["O"]:
            self.score += 1
            print("Food found! Score:", self.score)
        # find resource
        # go there
        return False


def init_agent(grid):
    agent = Agent()

    y = randrange(1, len(grid) - 1)
    x = randrange(1, len(grid[agent.y]) - 1)
    move_agent(agent, grid, x, y)
    return agent


def invalid_move(x, y):
    return x < 1 or x > 8 or y < 1 or y > 8


def move_agent(agent, grid, x, y):
    if invalid_move(x, y):
        return
    agent.x = x
    agent.y = y
    grid[agent.y][agent.x] = CELLS["P"]


def run():
    done = False
    grid = init_grid()
    agent = init_agent(grid)
    print_world(grid, agent)

    while not done:
        done = agent.act(grid)
        # print_world(grid, agent)


if __name__ == "__main__":
    run()

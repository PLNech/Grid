from agent import Agent
from world.grid import Grid


def run():
    run_i = 0
    done = False
    grid = Grid()
    agent = Agent()
    grid.add_agent(agent)
    print(str(grid))

    while not done:
        run_i += 1
        reward, done = agent.act(grid)
        print("Run %s: %s\n%s" % (run_i, reward, grid), flush=True)
    print("Done! Got %s points in %s rounds." % (agent.score, run_i))

if __name__ == "__main__":
    run()

#! /usr/bin/env python
import gym

EPISODES = 20
TIMESTEPS = 1000

games = {
    "pole": "CartPole-v0",
    "car": "MountainCar-v0",
    "dunk": "DoubleDunk-v0"
}
debug = {
    0: True,
    "observation": True,
}

env = gym.make(games["dunk"])
print("Actions:", env.action_space)
print("Observations: %s (%s -> %s)" % (env.observation_space, env.observation_space.low, env.observation_space.high))

for e in range(EPISODES):
    observation = env.reset()
    for _ in range(TIMESTEPS):
        env.render()
        action = env.action_space.sample()  # take a random action
        observation, reward, done, info = env.step(1)
        print("Action: ", action)
        print("Reward: ", reward)
        print("Observation: %s" % observation)
        print("Info: %s" % info)

        if done:
            print("Episode finished after {} timesteps".format(e + 1))
            env.reset()
env.close()

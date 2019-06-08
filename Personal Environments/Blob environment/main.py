import pygame
import pickle
from Agent import Agent
from Environment import Blob_Env 
import time

display_width, display_height = 200, 200

pygame.init()

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Blob Game')
clock = pygame.time.Clock()

#creating the environment
env = Blob_Env(gameDisplay, clock)

#initialising agent
agent = Agent(env = env,
              alpha = 0.1 )

#getting agent's policy
directory = 'policy3.pickle'
agent.set_policy(directory)

#testing the agent
for i in range(10):  #running for 10 times
    state = env.reset()
    total_reward = 0
    while True:
        #rendering the environment
        env.render()
        #decide action for present state
        action = agent.take_action(state)
        state, reward, done = env.step(action)
        total_reward += reward
        if done:
            time.sleep(2)
            print(total_reward)
            break 

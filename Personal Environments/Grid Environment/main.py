import pygame
import pickle
from Agent import Agent
from Environment import Grid_Env, Game_Matrix 
import time
import random

display_width, display_height = 200, 200

pygame.init()
pygame.display.set_caption('Grid environment')
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()


#initialising the game matrix
game_matrix = Game_Matrix()
#creating the environment
env = Grid_Env(gameDisplay, clock, game_matrix)

#initialising agent
agent = Agent(env = env,
              alpha = 0.5)

#uncomment 
#getting agent's policy
#directory = 'policy_default_env.pickle'
#agent.set_policy(directory)

#training the agent via interaction
agent.interact(num_episodes=2000)


#testing the agent
pygame.display.set_caption('Test Phase')
for i in range(10):  #running for 10 times
    state = env.reset()
    total_reward = 0
    while True:
        #detecting events on pygame window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()   #close the window
                quit()          #quit the program
        #rendering the environment
        env.render()
        #decide action for present state
        action = agent.take_action(state)    #change this to watch a random agent
        state, reward, done = env.step(action)
        total_reward += reward
        if done:
            time.sleep(2)
            print(total_reward)
            break 

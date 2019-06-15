#Environment
import pygame
import numpy as np 
import random
import time
from collections import deque 


#colours - r,g,b
WHITE = (255,255,255)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
TEXT_COLOR = (0,0,220)

class Grid_Env():

    def __init__(self, gameDisplay, clock, game_matrix):

        self.HEIGHT = game_matrix.ROWS  #height of the environment
        self.WIDTH = game_matrix.COLUMNS   #width of the environment
        
        self.STATE_SPACE = self.WIDTH * self.HEIGHT  #since agent can be in any one of the coordinates
        self.ACTION_SPACE = 4  #four movements
        self.MOVES = 20
            
        '''rendering specific variables'''
        self.DISPLAY = gameDisplay   #will be used for rendering
        self.CLOCK = clock
        display_width, display_height = gameDisplay.get_size()
        #defining blobs
        self.BLOB_WIDTH = int(display_width/5)
        self.BLOB_HEIGHT = int(display_height/5)
		#enemy
        self.ENEMY_WIDTH = int(display_width/5)
        self.ENEMY_HEIGHT = int(display_height/5)

        #positions
        self.START_POSITION = (0,0)
        self.GOAL_X, self.GOAL_Y = self.WIDTH-1, self.HEIGHT-1
        self.ENEMY_POSITIONS = game_matrix.ENEMY_POSITIONS


#--------------------------------------------Reset the environment--------------------------------------------------#
    
    def reset(self):
        self.MOVES = 100   #resetting the moves to 100
        self.STATE = self.START_POSITION #setting the agent to start position
        return self.STATE

#-----------------------------------------------Render the enviroment-----------------------------------------------#    

    def render(self, i_episode=-1):
        '''
            rendering the environment using pygame display
        '''

        self.DISPLAY.fill(BLACK)
        blob_x, blob_y = self.STATE
        #drawing blob - our agent
        pygame.draw.rect(self.DISPLAY, WHITE, [ blob_x*self.BLOB_WIDTH, blob_y*self.BLOB_HEIGHT, self.BLOB_WIDTH, self.BLOB_HEIGHT])
        #drwawing goal
        pygame.draw.rect(self.DISPLAY, GREEN, [ self.GOAL_X*self.ENEMY_WIDTH, self.GOAL_Y*self.ENEMY_HEIGHT, self.ENEMY_WIDTH, self.ENEMY_HEIGHT])
        #drawing enemies
        for pos in self.ENEMY_POSITIONS:
        	pygame.draw.rect(self.DISPLAY, RED, [pos[0]*self.ENEMY_WIDTH, pos[1]*self.ENEMY_HEIGHT, self.ENEMY_WIDTH, self.ENEMY_HEIGHT])

        if i_episode>=0:
            self.display_episode(i_episode)

        #updating the display
        pygame.display.update()
        self.CLOCK.tick(50)

#--------------------------------------Agent takes step and the environment changes------------------------------------#

    def step(self,action):

        reward = -1
        done = False

        #decreasing the no. of moves
        self.MOVES -= 1
        #done if moves =0
        if self.MOVES==0:
            done = True

        x_change, y_change = 0, 0
        #decide action
        if action == 0:
            x_change = -1  #moving left
        elif action == 1:
            x_change = 1   #moving right
        elif action == 2:
            y_change = -1 #moving upwards
        elif action ==3:
            y_change = 1  #moving downwards

        blob_x, blob_y = self.STATE

        #updating the blob position
        blob_x += x_change
        blob_y += y_change
        
        # If blob out of bounds, fix!
        if blob_x < 0:
            blob_x = 0
        elif blob_x > self.WIDTH-1:
            blob_x = self.WIDTH-1
        if blob_y < 0:
            blob_y = 0
        elif blob_y > self.HEIGHT -1:
            blob_y = self.HEIGHT -1
        
        #reached goal
        if blob_x == self.GOAL_X and blob_y == self.GOAL_Y:
            reward = 20  #may want to change this
            done = True

        #crashed into enemy
        for pos in self.ENEMY_POSITIONS:
        	if blob_x == pos[0] and blob_y == pos[1]:
        		reward = -10 #A negative reward
        		done = True    
        
        
        self.STATE = (blob_x, blob_y)

        return self.STATE, reward, done
        

#----------------------------Helper function to display episode-------------------------#

    def display_episode(self,epsiode):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Episode: "+str(epsiode), True, TEXT_COLOR)
        self.DISPLAY.blit(text,(1,1))		

#---- A helpful class GAME_MATRIX (Abstracts the specific features of game from environment)-------------------#


class Game_Matrix:

	def __init__(self, rows=5, columns=5):
		self.ROWS = rows 
		self.COLUMNS = columns
		self.ENEMY_POSITIONS = [[1,1], [3,1], [1,3], [3,3]]

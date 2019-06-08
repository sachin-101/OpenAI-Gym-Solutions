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

class Blob_Env():

    def __init__(self, gameDisplay, clock):

        self.HEIGHT = 10  #height of the environment
        self.WIDTH = 10   #width of the environment
        self.STATE_SPACE = (self.HEIGHT*self.WIDTH)*(self.HEIGHT*self.WIDTH - 1)   #number of states for two 
        self.ACTION_SPACE = 4
        self.DISPLAY = gameDisplay   #will be used for rendering
        self.CLOCK = clock

        #max blob moves
        self.MOVES = 100
        #getting the display width to set the blob and food size accordingly
        display_width, display_height = gameDisplay.get_size()
        #defining blobs
        self.BLOB_WIDTH = int(display_width/10)
        self.BLOB_HEIGHT = int(display_height/10)

        #food
        self.FOOD_WIDTH = int(display_width/10)
        self.FOOD_HEIGHT = int(display_height/10)


    def reset(self):

        self.MOVES = 100   #resetting the moves to 100
        state_x = tuple(np.random.random_integers(low=0, high=self.WIDTH-1, size=2))
        state_y = tuple(np.random.random_integers(low=0, high=self.HEIGHT-1, size=2))
        self.STATE = (state_x[0] - state_x[1] , state_y[0] - state_y[1])
        
        #blob position
        self.X, self.Y = state_x[0], state_y[0]
        self.X_f, self.Y_f = state_x[1], state_y[1]

        return self.STATE
    
    def render(self):
        '''
            NEED TO WORK MORE ON THIS
        '''

        self.DISPLAY.fill(BLACK)
        blob_x, food_x, blob_y, food_y = self.X, self.X_f, self.Y, self.Y_f
        #drawing snake
        pygame.draw.rect(self.DISPLAY, WHITE, [ blob_x*self.BLOB_WIDTH, blob_y*self.BLOB_HEIGHT, self.BLOB_WIDTH, self.BLOB_HEIGHT])
        #drawing food
        pygame.draw.rect(self.DISPLAY, BLUE, [food_x*self.FOOD_WIDTH, food_y*self.FOOD_HEIGHT, self.FOOD_WIDTH, self.FOOD_HEIGHT])

        #updating the display
        pygame.display.update()
        self.CLOCK.tick(20)

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

        blob_x, blob_y = self.X, self.Y

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

        self.X, self.Y = blob_x, blob_y
        
        if blob_x == self.X_f and blob_y == self.Y_f:
            reward = 10  #may want to change this
            done = True

        
        
        self.STATE = (self.X - self.X_f, self.Y - self.Y_f)

        return self.STATE, reward, done
        
         




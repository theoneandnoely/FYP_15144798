'''
Created on 5 Nov 2019

@author: Noel
'''

from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import MultiGrid
from agent import Player, Ball, Goal
from potential import goalV, ballV
import potential

class Model(Model):
    '''
    classdocs
    '''


    def __init__(self, teams, players, height=136, width=210):
        '''
        Create a playing area of (height, width) cells.
        '''
        
        # Use SimultaneousActivation which simulates all the cells
        # computing their next state simultaneously.  This needs to
        # be done because each cell's next state depends on the current
        # state of all its neighbors -- before they've changed.
        self.schedule = SimultaneousActivation(self)
        
        #Using a MultiGrid where agents can occupy the same cell and the edges don't wrap
        self.grid = MultiGrid(width, height, False)
        self.numTeams = teams
        self.players = players
        
        #Place Goals
        xG = 0
        yG = 60
        for k in range(16):
            a = Goal(xG, yG+k, potential.goalV(xG,yG+k), self)
            b = Goal(xG+width, yG+k, potential.goalV(xG+width, yG+k), self)
            self.grid.place_agent(a,(xG, yG+k))
            self.grid.place_agent(b,(xG+width, yG+k))
        
        for i in range(self.numTeams):
            for j in range(self.players):
                if j == 0:
                    a = Player()
            
        

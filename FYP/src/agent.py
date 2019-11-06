'''
Created on 6 Nov 2019

@author: Noel
'''
from mesa import Agent

class Player(Agent):
    '''
    classdocs
    '''


    def __init__(self, teamID, playerID, status, vField, model):
        '''
        Constructor
        '''
        self.teamID = teamID
        self.playerID = playerID
        self.status = status
        self.vField = vField
        
class Ball(Agent):
    
    def __init__(self, vField, model):
        self.vField = vField
        
class Goal(Agent):
    
    def __init__(self, xPos, yPos, vField, model):
        self.xPos = xPos
        self.yPos = yPos
        self.vField = vField


# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:40:31 2020

@author: Noel
"""


from mesa import Agent
import numpy as np
from random import randint
#from BallAgent import *

class PlayerAgent(Agent):
    def __init__(self, unique_id, model, goalkeeper = False, possession = False):
        super().__init__(unique_id, model)
        if (unique_id % 2 == 0):
            self.teamID = 1
        else:
            self.teamID = 2
        self.maxDisp = 0
        self.stepsX = []
        self.stepsY = []
        self.dispPerStep = []
        self.avgDisp = 0
        self.goalkeeper = goalkeeper
        self.possession = possession
 
    '''       
    def checkPossession(self):
        contents = self.model.grid.get_cell_list_contents(self.pos)
        for i in range(len(contents)):
            if type(contents[i]) == BallAgent:
                possession = True
                break
            else:
                possession = False
        return possession
    '''           
        
        
    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore = False,
            include_center = True
        )
        newPosition = self.random.choice(possibleSteps)
        (x0,y0) = self.pos
        (x,y)=newPosition
        xDiff = x - x0
        self.stepsX.append(xDiff)
        yDiff = y - y0
        self.stepsY.append(yDiff)
        if newPosition != self.pos:
            self.model.grid.move_agent(self, newPosition)
        else:
            pass
        #return self.maxDisp, self.dispPerStep
        
    def displacement(self):
        disp = 0
        sumX = sum(self.stepsX)
        sumY = sum(self.stepsY)
        disp = ((sumX)**2 + (sumY)**2)**0.5
        self.dispPerStep.append(disp)
    
    def averageDisp(self):
        if len(self.dispPerStep) > 0:
            return sum(self.dispPerStep)/len(self.dispPerStep)
        else:
            return 0
    
    def maxDisplacement(self):
        maxDisp = self.maxDisp
        for i in range(len(self.dispPerStep)):
            if self.dispPerStep[i] > maxDisp:
                maxDisp = self.dispPerStep[i]
        return maxDisp
    
    def getPotential(self):
        (x,y) = self.pos
        if self.teamID == 1:
            if self.goalkeeper == True:
                vStay = self.model.goalPotential2[x][y]
                vUp = self.model.goalPotential2[x][y-1]
                vDown = self.model.goalPotential2[x][y+1]
                vRight = self.model.goalPotential2[x-1][y]
                vLeft = self.model.goalPotential2[x+1][y]
            else:
                vStay = self.model.goalPotential1[x][y]
                vUp = self.model.goalPotential1[x][y-1]
                vDown = self.model.goalPotential1[x][y+1]
                vRight = self.model.goalPotential1[x-1][y]
                vLeft = self.model.goalPotential1[x+1][y]
        else:
            if self.goalkeeper == True:
                vStay = self.model.goalPotential1[x][y]
                vUp = self.model.goalPotential1[x][y+1]
                vDown = self.model.goalPotential1[x][y-1]
                vRight = self.model.goalPotential1[x+1][y]
                vLeft = self.model.goalPotential1[x-1][y]
            else:
                vStay = self.model.goalPotential2[x][y]
                vUp = self.model.goalPotential2[x][y+1]
                vDown = self.model.goalPotential2[x][y-1]
                vRight = self.model.goalPotential2[x+1][y]
                vLeft = self.model.goalPotential2[x-1][y]
        return (vStay,vUp,vDown,vRight,vLeft)
    
    def shoot(self):
        shotThreshold = 5000 #Arbitrary and Needs to be chosen once potential fields are calculated
        (x,y) = self.pos
        if self.teamID == 1:
            if self.model.goalPotential2[x][y] < shotThreshold:
                g = shotThreshold - self.model.goalPotential2[x][y]
                s = randint(0,shotThreshold)
                if g > s:
                    self.model.score1 = self.model.score1 + 1
                    #reset Positions function needed
                else:
                    #move ball to GK position
                    pass
            else:
                pass
        else:
            if self.model.goalPotential1[x][y] < shotThreshold:
                g = shotThreshold - self.model.goalPotential1[x][y]
                s = randint(0,shotThreshold)
                if g > s:
                    self.model.score2 = self.model.score2 + 1
                    #reset Positions function needed
                else:
                    #move ball to GK position
                    pass
            else:
                pass
    
    def passBall(self):
        '''
        for every goalPotential < self.goalPotential:
            get cell contents
            if cell contains playerAgent with teamID == self.teamID:
                listOfPassOptions.append([x,y])
        for min(listOfPassOptions):
            if passPotential < passThreshold:
                ballPos == targetPos
            else:
                repeat for nextMinimum
        '''
        pass
    
    def tackle(self):
        '''
        getNeighborhood
        if ballAgent is in nextCell:
            take possession of ballAgent
        '''
        pass
    
    def bugTest(self):
        idS = str(self.unique_id)
        print("Unique ID: " + idS)
        team = str(self.teamID)
        print("Team: " + team)
        (x,y) = self.pos
        xStr = str(x)
        yStr = str(y)
        print("X: " + xStr)
        print("Y: " + yStr)
        if self.goalkeeper is True:
            print("(GK)")
        if self.possession == True:
            print("In Possession")
        #potential = self.getPotential()
        #potS = str(potential)
        #print("V: " + potS)
    
    def step(self):
        #self.shoot()
        #self.passBall()
        #self.tackle()
        self.displacement()
        self.avgDisp = self.averageDisp()
        self.maxDisp = self.maxDisplacement()
        self.bugTest()
        
    def advance(self):
        self.move()
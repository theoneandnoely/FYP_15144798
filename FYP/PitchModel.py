# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:32:43 2020

@author: Noel
"""


from mesa import Model #Import Model Class from mesa package
from mesa.space import MultiGrid #Import grid to allow multiple agents to occupy the same cell
from mesa.time import SimultaneousActivation #Schedule such that each agent moves simultaneously
from mesa.datacollection import DataCollector
from PlayerAgent import *
#from BallAgent import *
import numpy as np
import matplotlib.pyplot as plt

class PitchModel(Model):
    def __init__(self, N, width, height):
        '''Initiate the model'''
        self.num_agents = 2*N
        self.grid = MultiGrid(width, height, False)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.justConceded = 0
        self.score1 = 0
        self.score2 = 0
        
        #Set initial potential field due to goals
        self.goalPotential1 = np.zeros((width, height))
        self.goalPotential2 = np.zeros((width, height))
        for x in range(8):
            for y in range(height):
                widthVal = ((width/2)-4) + x
                self.goalPotential1[int(widthVal)][y] = (y+1)*10
                self.goalPotential2[int(widthVal)][height-(y+1)] = (y+1)*10
        for x in range(int((width/2)-4)):
            for y in range(height):
                r = (((x+1)**2)+((y+1)**2))**0.5
                goalStart = ((width/2)-5) -x
                goalEnd = ((width/2)+4) + x
                self.goalPotential1[int(goalStart)][y] = r*10
                self.goalPotential1[int(goalEnd)][y] = r*10
                self.goalPotential2[int(goalStart)][height-(y+1)] = r*10
                self.goalPotential2[int(goalEnd)][height-(y+1)] = r*10
        
        #Create Agents
        for i in range(self.num_agents):
            if i > ((2*N)-3):
                a = PlayerAgent(i,self,True)
            else:
                a = PlayerAgent(i,self)
            self.schedule.add(a)
            
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x,y))
            
        #Set Up Kickoff
        self.kickoff()
        
        #Set Up DataCollector
        self.datacollector = DataCollector(
            model_reporters={"Score 1":"score1","Score 2":"score2"},
            agent_reporters={"Avg. Displacement":"avgDisp", "Max Displacement":"maxDisp"}
        )
        
    def kickoff(self):
        posBoy = -1
        newPositions = {}
        if self.justConceded == 0:
            posTeam = self.random.randint(1,3)
        else:
            posTeam = self.justConceded
        for cellContents, x, y in self.grid.coord_iter():
            if len(cellContents) == 0:
                pass
            else:
                for i in cellContents:
                    if posBoy == -1:
                        if i.teamID == posTeam:
                            if i.goalkeeper == True:
                                pass
                            else:
                                i.possession = True
                                posBoy = i.unique_id
                                newPositions[i] = ((self.grid.width/2)-1,(self.grid.height/2)-1)
                    if i.unique_id != posBoy:
                        if i.teamID == 1:
                            if i.goalkeeper == True:
                                x = self.random.randint((self.grid.width/2)-5,(self.grid.width/2)+4)
                                y = self.random.randint(0,17)
                                newPositions[i] = (x,y)
                            else:
                                x = self.random.randrange(self.grid.width)
                                y = self.random.randint(0,(self.grid.height/2)-1)
                                newPositions[i] = (x,y)
                        else:
                            if i.goalkeeper == True:
                                x = self.random.randint((self.grid.width/2)-5,(self.grid.width/2)+4)
                                y = self.random.randint(self.grid.height - 18,self.grid.height-1)
                                newPositions[i] = (x,y)
                            else:
                                x = self.random.randrange(self.grid.width)
                                y = self.random.randint((self.grid.height/2)-1, self.grid.height-1)
                                newPositions[i] = (x,y)
        for key in newPositions.keys():
            (x,y) = newPositions[key]
            x = int(x)
            y = int(y)
            self.grid.move_agent(key,(x,y))
            
        
    def calcPotential(self):
        playerPos = {}
        for agent, x, y in self.grid.coord_iter():
            if len(agent) == 0:
                pass
            else:
                for i in agent:
                    playerPos[i.unique_id] = {"x":x,"y":y,"team ID":i.teamID, "possession":i.possession}
        for key in playerPos.keys():
            agent = playerPos[key]
            potential = np.zeros((self.grid.width, self.grid.height))
            negRangeX = agent['x']
            negRangeY = agent['y']
            posRangeX = self.grid.width - (agent['x']+1)
            posRangeY = self.grid.height - (agent['y']+1)
                
            if agent['team ID'] == 1:
                for i in range(negRangeX):
                    for j in range(negRangeY):
                        negX = agent['x']-(i+1)
                        negY = agent['y']-(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[negX][negY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                    for j in range(posRangeY):
                        negX = agent['x']-(i+1)
                        posY = agent['y']+(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[negX][posY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                for i in range(posRangeX):
                    for j in range(negRangeX):
                        posX = agent['x']+(i+1)
                        negY = agent['y']-(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[posX][negY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                    for j in range(posRangeY):
                        posX = agent['x']+(i+1)
                        posY = agent['y']+(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[posX][posY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                for i in range(self.grid.width):
                    for j in range(self.grid.height):
                        self.goalPotential1[i][j] = self.goalPotential1[i][j] - potential[i][j]
                        self.goalPotential2[i][j] = self.goalPotential2[i][j] + potential[i][j]
            elif agent['team ID'] == 2:
                for i in range(negRangeX):
                    for j in range(negRangeY):
                        negX = agent['x']-(i+1)
                        negY = agent['y']-(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[negX][negY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                    for j in range(posRangeY):
                        negX = agent['x']-(i+1)
                        posY = agent['y']+(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[negX][posY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                for i in range(posRangeX):
                    for j in range(negRangeX):
                        posX = agent['x']+(i+1)
                        negY = agent['y']-(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[posX][negY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                    for j in range(posRangeY):
                        posX = agent['x']+(i+1)
                        posY = agent['y']+(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[posX][posY] = 400*((((2**(-1/6))/r)**12)-(((2**(-1/6))/r)**6))
                for i in range(self.grid.width):
                    for j in range(self.grid.height):
                        self.goalPotential2[i][j] = self.goalPotential2[i][j] - potential[i][j]
                        self.goalPotential1[i][j] = self.goalPotential1[i][j] + potential[i][j]
            if agent['possession'] == True:
                for i in range(negRangeX):
                    for j in range(negRangeY):
                        negX = agent['x']-(i+1)
                        negY = agent['y']-(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[negX][negY] = potential[negX][negY] + ((r/2)**2)
                    for j in range(posRangeY):
                        negX = agent['x']-(i+1)
                        posY = agent['y']+(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[negX][posY] = potential[negX][posY] + ((r/2)**2)
                for i in range(posRangeX):
                    for j in range(negRangeX):
                        posX = agent['x']+(i+1)
                        negY = agent['y']-(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[posX][negY] = potential[posX][negY] + ((r/2)**2)
                    for j in range(posRangeY):
                        posX = agent['x']+(i+1)
                        posY = agent['y']+(j+1)
                        r = ((i+1)**2+(j+1)**2)**(0.5)
                        potential[posX][posY] = potential[posX][posY] + ((r/2)**2)
                plt.figure(1)
                plt.clf()
                plt.imshow(potential, interpolation="nearest")
                for i in range(self.grid.width):
                    for j in range(self.grid.height):
                        self.goalPotential1[i][j] = self.goalPotential1[i][j] + potential[i][j]
                        self.goalPotential2[i][j] = self.goalPotential2[i][j] + potential[i][j]
        
    def scoreCheck(self):
        '''Checks if any player agent has successfully scored and increments the team's score by 1'''
        score1 = self.score1
        score2 = self.score2
        #if playerAgent.shoot returns True
            #if teamID = 1
                #score1 += 1
            #else
                #score2 += 1
        return score1, score2
            
    def bugTest(self):
        self.calcPotential()
        plt.figure(3)
        plt.clf()
        plt.imshow(self.goalPotential1, interpolation="nearest")
        plt.figure(4)
        plt.clf()
        plt.imshow(self.goalPotential2, interpolation="nearest")
        
    def step(self):
        '''Advance the model by one step.'''
        self.scoreCheck()
        self.datacollector.collect(self)
        self.schedule.step()
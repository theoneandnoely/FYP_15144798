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
        self.i = 0
        self.newPossession = -1
        
        #Initialise potential fields for each state
        self.movePotentialGK1 = np.zeros((width, height))
        self.movePotentialGK2 = np.zeros((width, height))
        self.movePotentialGKP1 = np.zeros((width, height))
        self.movePotentialGKP2 = np.zeros((width, height))
        self.movePotentialDF1 = np.zeros((width, height))
        self.movePotentialDF2 = np.zeros((width, height))
        self.movePotentialPO1 = np.zeros((width, height))
        self.movePotentialPO2 = np.zeros((width, height))
        self.movePotentialBP1 = np.zeros((width, height))
        self.movePotentialBP2 = np.zeros((width, height))
        
        #Set initial potential field due to goals
        self.goalPotentialGK1 = np.zeros((width, height))
        self.goalPotentialGK2 = np.zeros((width, height))
        self.goalPotentialGKP1 = np.zeros((width, height))
        self.goalPotentialGKP2 = np.zeros((width, height))
        self.goalPotentialDF1 = np.zeros((width, height))
        self.goalPotentialDF2 = np.zeros((width, height))
        self.goalPotentialPO1 = np.zeros((width, height))
        self.goalPotentialPO2 = np.zeros((width, height))
        self.goalPotentialBP1 = np.zeros((width, height))
        self.goalPotentialBP2 = np.zeros((width, height))
        
        for x in range(8):
            for y in range(height):
                widthVal = ((width/2)-4) + x
                self.goalPotentialGK1[int(widthVal)][y] = self.goalPotentialGK1[int(widthVal)][y] + (y+1)
                self.goalPotentialGK1[int(widthVal)][height-(y+1)] = self.goalPotentialGK1[int(widthVal)][height-(y+1)] - np.log2(height-(y+1))
                
                self.goalPotentialGK2[int(widthVal)][y] = self.goalPotentialGK2[int(widthVal)][y] - np.log2(height-(y+1))
                self.goalPotentialGK2[int(widthVal)][height-(y+1)] = self.goalPotentialGK2[int(widthVal)][height-(y+1)] + (y+1)
                
                self.goalPotentialGKP1[int(widthVal)][y] = self.goalPotentialGKP1[int(widthVal)][y] + (y+1)
                self.goalPotentialGKP1[int(widthVal)][height-(y+1)] = self.goalPotentialGKP1[int(widthVal)][height-(y+1)] - np.log2(height-(y+1))
                
                self.goalPotentialGKP2[int(widthVal)][y] = self.goalPotentialGKP2[int(widthVal)][y] - np.log2(height-(y+1))
                self.goalPotentialGKP2[int(widthVal)][height-(y+1)] = self.goalPotentialGKP2[int(widthVal)][height-(y+1)] + (y+1)
                
                self.goalPotentialDF1[int(widthVal)][y] = self.goalPotentialDF1[int(widthVal)][y] + (y+1)
                self.goalPotentialDF1[int(widthVal)][height-(y+1)] = self.goalPotentialDF1[int(widthVal)][height-(y+1)] - np.log2(height-(y+1))
                
                self.goalPotentialDF2[int(widthVal)][y] = self.goalPotentialDF2[int(widthVal)][y] - np.log2(height-(y+1))
                self.goalPotentialDF2[int(widthVal)][height-(y+1)] = self.goalPotentialDF2[int(widthVal)][height-(y+1)] + (y+1)
                
                self.goalPotentialPO1[int(widthVal)][y] = self.goalPotentialPO1[int(widthVal)][y] - np.log2(height-(y+1))
                self.goalPotentialPO1[int(widthVal)][height-(y+1)] = self.goalPotentialPO1[int(widthVal)][height-(y+1)] + (y+1)
                
                self.goalPotentialPO2[int(widthVal)][y] = self.goalPotentialPO2[int(widthVal)][y] + (y+1)
                self.goalPotentialPO2[int(widthVal)][height-(y+1)] = self.goalPotentialPO2[int(widthVal)][height-(y+1)] - np.log2(height-(y+1))
                
                self.goalPotentialBP1[int(widthVal)][y] = self.goalPotentialBP1[int(widthVal)][y] - np.log2(height-(y+1))
                self.goalPotentialBP1[int(widthVal)][height-(y+1)] = self.goalPotentialBP1[int(widthVal)][height-(y+1)] + (y+1)
                
                self.goalPotentialBP2[int(widthVal)][y] = self.goalPotentialBP2[int(widthVal)][y] + (y+1)
                self.goalPotentialBP2[int(widthVal)][height-(y+1)] = self.goalPotentialBP2[int(widthVal)][height-(y+1)] - np.log2(height-(y+1))
                
        for x in range(int((width/2)-4)):
            for y in range(height):
                r1 = (((x+1)**2)+((y+1)**2))**0.5
                r2 = (((x+1)**2)+((height-(y+1))**2))**0.5
                goalStart = ((width/2)-5) -x
                goalEnd = ((width/2)+4) + x
                
                self.goalPotentialGK1[int(goalStart)][y] = self.goalPotentialGK1[int(goalStart)][y] + (r1)
                self.goalPotentialGK1[int(goalEnd)][y] = self.goalPotentialGK1[int(goalEnd)][y] + (r1)
                self.goalPotentialGK1[int(goalStart)][height-(y+1)] = self.goalPotentialGK1[int(goalStart)][height-(y+1)] - np.log2(r2)
                self.goalPotentialGK1[int(goalEnd)][height-(y+1)] = self.goalPotentialGK1[int(goalEnd)][height-(y+1)] - np.log2(r2)
                
                self.goalPotentialGK2[int(goalStart)][y] = self.goalPotentialGK2[int(goalStart)][y] - np.log2(r2)
                self.goalPotentialGK2[int(goalEnd)][y] = self.goalPotentialGK2[int(goalEnd)][y] - np.log2(r2)
                self.goalPotentialGK2[int(goalStart)][height-(y+1)] = self.goalPotentialGK2[int(goalStart)][height-(y+1)] + (r1)
                self.goalPotentialGK2[int(goalEnd)][height-(y+1)] = self.goalPotentialGK2[int(goalEnd)][height-(y+1)] + (r1)
                
                self.goalPotentialGKP1[int(goalStart)][y] = self.goalPotentialGKP1[int(goalStart)][y] + (r1)
                self.goalPotentialGKP1[int(goalEnd)][y] = self.goalPotentialGKP1[int(goalEnd)][y] + (r1)
                self.goalPotentialGKP1[int(goalStart)][height-(y+1)] = self.goalPotentialGKP1[int(goalStart)][height-(y+1)] - np.log2(r2)
                self.goalPotentialGKP1[int(goalEnd)][height-(y+1)] = self.goalPotentialGKP1[int(goalEnd)][height-(y+1)] - np.log2(r2)
                
                self.goalPotentialGKP2[int(goalStart)][y] = self.goalPotentialGKP2[int(goalStart)][y] - np.log2(r2)
                self.goalPotentialGKP2[int(goalEnd)][y] = self.goalPotentialGKP2[int(goalEnd)][y] - np.log2(r2)
                self.goalPotentialGKP2[int(goalStart)][height-(y+1)] = self.goalPotentialGKP2[int(goalStart)][height-(y+1)] + (r1)
                self.goalPotentialGKP2[int(goalEnd)][height-(y+1)] = self.goalPotentialGKP2[int(goalEnd)][height-(y+1)] + (r1)
                
                self.goalPotentialDF1[int(goalStart)][y] = self.goalPotentialDF1[int(goalStart)][y] + (r1)
                self.goalPotentialDF1[int(goalEnd)][y] = self.goalPotentialDF1[int(goalEnd)][y] + (r1)
                self.goalPotentialDF1[int(goalStart)][height-(y+1)] = self.goalPotentialDF1[int(goalStart)][height-(y+1)] - np.log2(r2)
                self.goalPotentialDF1[int(goalEnd)][height-(y+1)] = self.goalPotentialDF1[int(goalEnd)][height-(y+1)] - np.log2(r2)
                
                self.goalPotentialDF2[int(goalStart)][y] = self.goalPotentialDF2[int(goalStart)][y] - np.log2(r2)
                self.goalPotentialDF2[int(goalEnd)][y] = self.goalPotentialDF2[int(goalEnd)][y] - np.log2(r2)
                self.goalPotentialDF2[int(goalStart)][height-(y+1)] = self.goalPotentialDF2[int(goalStart)][height-(y+1)] + (r1)
                self.goalPotentialDF2[int(goalEnd)][height-(y+1)] = self.goalPotentialDF2[int(goalEnd)][height-(y+1)] + (r1)
                
                self.goalPotentialPO1[int(goalStart)][y] = self.goalPotentialPO1[int(goalStart)][y] - np.log2(r2)
                self.goalPotentialPO1[int(goalEnd)][y] = self.goalPotentialPO1[int(goalEnd)][y] - np.log2(r2)
                self.goalPotentialPO1[int(goalStart)][height-(y+1)] = self.goalPotentialPO1[int(goalStart)][height-(y+1)] + (r1)
                self.goalPotentialPO1[int(goalEnd)][height-(y+1)] = self.goalPotentialPO1[int(goalEnd)][height-(y+1)] + (r1)
                
                self.goalPotentialPO2[int(goalStart)][y] = self.goalPotentialPO2[int(goalStart)][y] + (r1)
                self.goalPotentialPO2[int(goalEnd)][y] = self.goalPotentialPO2[int(goalEnd)][y] + (r1)
                self.goalPotentialPO2[int(goalStart)][height-(y+1)] = self.goalPotentialPO2[int(goalStart)][height-(y+1)]  - np.log2(r2)
                self.goalPotentialPO2[int(goalEnd)][height-(y+1)] = self.goalPotentialPO2[int(goalEnd)][height-(y+1)] - np.log2(r2)
                
                self.goalPotentialBP1[int(goalStart)][y] = self.goalPotentialBP1[int(goalStart)][y] - np.log2(r2)
                self.goalPotentialBP1[int(goalEnd)][y] = self.goalPotentialBP1[int(goalEnd)][y] - np.log2(r2)
                self.goalPotentialBP1[int(goalStart)][height-(y+1)] = self.goalPotentialBP1[int(goalStart)][height-(y+1)] + (r1)
                self.goalPotentialBP1[int(goalEnd)][height-(y+1)] = self.goalPotentialBP1[int(goalEnd)][height-(y+1)] + (r1)
                
                self.goalPotentialBP2[int(goalStart)][y] = self.goalPotentialBP2[int(goalStart)][y] + (r1)
                self.goalPotentialBP2[int(goalEnd)][y] = self.goalPotentialBP2[int(goalEnd)][y] + (r1)
                self.goalPotentialBP2[int(goalStart)][height-(y+1)] = self.goalPotentialBP2[int(goalStart)][height-(y+1)] - np.log2(r2)
                self.goalPotentialBP2[int(goalEnd)][height-(y+1)] = self.goalPotentialBP2[int(goalEnd)][height-(y+1)] - np.log2(r2)
        
        
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
            posTeam = self.random.randint(1,2)
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
                                x = self.random.randint((self.grid.width/2)-5,(self.grid.width/2)+3)
                                y = self.random.randint(0,17)
                                newPositions[i] = (x,y)
                            else:
                                x = self.random.randrange(self.grid.width)
                                y = self.random.randint(0,(self.grid.height/2)-1)
                                newPositions[i] = (x,y)
                        else:
                            if i.goalkeeper == True:
                                x = self.random.randint((self.grid.width/2)-5,(self.grid.width/2)+3)
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
        self.justConceded = 0
            
        
    def calcPotential(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                self.movePotentialGK1[x][y] = self.goalPotentialGK1[x][y]
                self.movePotentialGK2[x][y] = self.goalPotentialGK2[x][y]
                
                self.movePotentialGKP1[x][y] = self.goalPotentialGKP1[x][y]
                self.movePotentialGKP2[x][y] = self.goalPotentialGKP2[x][y]
                
                self.movePotentialDF1[x][y] = self.goalPotentialDF1[x][y]
                self.movePotentialDF2[x][y] = self.goalPotentialDF2[x][y]
                
                self.movePotentialPO1[x][y] = self.goalPotentialPO1[x][y]
                self.movePotentialPO2[x][y] = self.goalPotentialPO2[x][y]
                
                self.movePotentialBP1[x][y] = self.goalPotentialBP1[x][y]
                self.movePotentialBP2[x][y] = self.goalPotentialBP2[x][y]
                
        playerPos = {}
        for agent, x, y in self.grid.coord_iter():
            if len(agent) == 0:
                pass
            else:
                for i in agent:
                    playerPos[i.unique_id] = {"x":x,"y":y, "state":i.state}
                    if i.state == "":
                        i.checkState()
                        playerPos[i.unique_id]['state'] = i.state
        for key in playerPos.keys():
            agent = playerPos[key]
            
            for i in range(self.grid.width):
                for j in range(self.grid.height):
                    r = ((agent['x']-i)**2+(agent['y']-j)**2)**(0.5)
                    if r != 0:
                        if agent['state'] == "GK":
                            self.movePotentialGK1[i][j] = self.movePotentialGK1[i][j] + (20/(r**2))
                            self.movePotentialGK2[i][j] = self.movePotentialGK2[i][j] + (20/(r**2))
                            
                            self.movePotentialGKP1[i][j] = self.movePotentialGKP1[i][j] + (20/(r**2))
                            self.movePotentialGKP2[i][j] = self.movePotentialGKP2[i][j] + (20/(r**2))
                            
                            self.movePotentialDF1[i][j] = self.movePotentialDF1[i][j] + 40*((5*(2**(-1/6))/r)**12-(5*(2**(-1/6))/r)**6)
                            self.movePotentialDF2[i][j] = self.movePotentialDF2[i][j] + 40*((5*(2**(-1/6))/r)**12-(5*(2**(-1/6))/r)**6)
                            
                            self.movePotentialPO1[i][j] = self.movePotentialPO1[i][j] + (20/(r**2))
                            self.movePotentialPO2[i][j] = self.movePotentialPO2[i][j] + (20/(r**2))
                            
                            self.movePotentialBP1[i][j] = self.movePotentialBP1[i][j] + (20/(r**2))
                            self.movePotentialBP2[i][j] = self.movePotentialBP2[i][j] + (20/(r**2))
                            
                        elif agent['state'] == "GKP":
                            self.movePotentialGK1[i][j] = self.movePotentialGK1[i][j] + (20/(r**2))
                            self.movePotentialGK2[i][j] = self.movePotentialGK2[i][j]  + (20/(r**2))
                            
                            self.movePotentialGKP1[i][j] = self.movePotentialGKP1[i][j]
                            self.movePotentialGKP2[i][j] = self.movePotentialGKP2[i][j]
                            
                            self.movePotentialDF1[i][j] = self.movePotentialDF1[i][j] + (20/(r**2))
                            self.movePotentialDF2[i][j] = self.movePotentialDF2[i][j] + (20/(r**2))
                            
                            self.movePotentialPO1[i][j] = self.movePotentialPO1[i][j] + (20/(r**2))
                            self.movePotentialPO2[i][j] = self.movePotentialPO2[i][j] + (20/(r**2))
                            
                            self.movePotentialBP1[i][j] = self.movePotentialBP1[i][j]
                            self.movePotentialBP2[i][j] = self.movePotentialBP2[i][j]
                            
                        elif agent['state'] == "DF":
                            self.movePotentialGK1[i][j] = self.movePotentialGK1[i][j] + (20/(r**2))
                            self.movePotentialGK2[i][j] = self.movePotentialGK2[i][j] + (20/(r**2))
                            
                            self.movePotentialGKP1[i][j] = self.movePotentialGKP1[i][j] + (20/(r**2))
                            self.movePotentialGKP2[i][j] = self.movePotentialGKP2[i][j] + (20/(r**2))
                            
                            self.movePotentialDF1[i][j] = self.movePotentialDF1[i][j] + (20/(r**2))
                            self.movePotentialDF2[i][j] = self.movePotentialDF2[i][j] + (20/(r**2))
                            
                            self.movePotentialPO1[i][j] = self.movePotentialPO1[i][j] + (20/(r**2))
                            self.movePotentialPO2[i][j] = self.movePotentialPO2[i][j] + (20/(r**2))
                            
                            self.movePotentialBP1[i][j] = self.movePotentialBP1[i][j] + (20/(r**2))
                            self.movePotentialBP2[i][j] = self.movePotentialBP2[i][j] + (20/(r**2))
                            
                        elif agent['state'] == "PO":
                            self.movePotentialGK1[i][j] = self.movePotentialGK1[i][j] - (20/(r**2))
                            self.movePotentialGK2[i][j] = self.movePotentialGK2[i][j] - (20/(r**2))
                            
                            self.movePotentialGKP1[i][j] = self.movePotentialGKP1[i][j] - (20/(r**2))
                            self.movePotentialGKP2[i][j] = self.movePotentialGKP2[i][j] - (20/(r**2))
                            
                            self.movePotentialDF1[i][j] = self.movePotentialDF1[i][j] + 40*((2.5*(2**(-1/6))/r)**12-(2.5*(2**(-1/6))/r)**6)
                            self.movePotentialDF2[i][j] = self.movePotentialDF2[i][j] + 40*((2.5*(2**(-1/6))/r)**12-(2.5*(2**(-1/6))/r)**6)
                            
                            self.movePotentialPO1[i][j] = self.movePotentialPO1[i][j] + (20/(r**2))
                            self.movePotentialPO2[i][j] = self.movePotentialPO2[i][j] + (20/(r**2))
                            
                            self.movePotentialBP1[i][j] = self.movePotentialBP1[i][j] + (20/(r**2))
                            self.movePotentialBP2[i][j] = self.movePotentialBP2[i][j] + (20/(r**2))
                            
                        elif agent['state'] == "BP":
                            self.movePotentialGK1[i][j] = self.movePotentialGK1[i][j] - (20/(r**2))
                            self.movePotentialGK2[i][j] = self.movePotentialGK2[i][j] - (20/(r**2))
                            
                            self.movePotentialGKP1[i][j] = self.movePotentialGKP1[i][j]
                            self.movePotentialGKP2[i][j] = self.movePotentialGKP2[i][j]
                            
                            self.movePotentialDF1[i][j] = self.movePotentialDF1[i][j] - (20/(r**2))
                            self.movePotentialDF2[i][j] = self.movePotentialDF2[i][j] - (20/(r**2))
                            
                            self.movePotentialPO1[i][j] = self.movePotentialPO1[i][j] + 40*((5*(2**(-1/6))/r)**12-(5*(2**(-1/6))/r)**6)
                            self.movePotentialPO2[i][j] = self.movePotentialPO2[i][j] + 40*((5*(2**(-1/6))/r)**12-(5*(2**(-1/6))/r)**6)
                            
                            self.movePotentialBP1[i][j] = self.movePotentialBP1[i][j]
                            self.movePotentialBP2[i][j] = self.movePotentialBP2[i][j]
                            
                        else:
                            print("Error in CalcPotential: Player has no state")
            
        
    def scoreCheck(self):
        '''Checks if any player agent has successfully scored and increments the team's score by 1'''
        if self.justConceded == 0:
            pass
        else:
            if self.justConceded == 1:
                self.score2 = self.score2 + 1
                self.kickoff()
            else:
                self.score1 = self.score1 + 1
                self.kickoff()
            
    def gridVisual(self):
        grid = np.zeros((self.grid.width, self.grid.height))
        for agent, x, y in self.grid.coord_iter():
            if len(agent) != 0:
                for k in agent:
                    grid[x][y] = k.teamID
        name = "Visualisation\Latest Test\Figure_"+str(self.i)+".jpg"
        plt.imsave(name, grid)
        
        
    def bugTest(self):
        self.calcPotential()
        plt.figure(1)
        plt.clf()
        plt.imshow(self.movePotentialBP1, interpolation = "nearest")
        
        plt.figure(2)
        plt.clf()
        plt.imshow(self.movePotentialBP2, interpolation = "nearest")
        
        plt.figure(3)
        plt.clf()
        plt.imshow(self.movePotentialDF1, interpolation = "nearest")
        
        plt.figure(4)
        plt.clf()
        plt.imshow(self.movePotentialDF2, interpolation = "nearest")
        
        plt.figure(5)
        plt.clf()
        plt.imshow(self.movePotentialGK1, interpolation = "nearest")
        
        plt.figure(6)
        plt.clf()
        plt.imshow(self.movePotentialGK2, interpolation = "nearest")
        
        plt.figure(7)
        plt.clf()
        plt.imshow(self.movePotentialGKP1, interpolation = "nearest")
        
        plt.figure(8)
        plt.clf()
        plt.imshow(self.movePotentialGKP2, interpolation = "nearest")
        
        plt.figure(9)
        plt.clf()
        plt.imshow(self.movePotentialPO1, interpolation = "nearest")
        
        plt.figure(10)
        plt.clf()
        plt.imshow(self.movePotentialPO2, interpolation = "nearest")
        
    def step(self):
        '''Advance the model by one step.'''
        self.calcPotential()
        self.scoreCheck()
        self.datacollector.collect(self)
        self.schedule.step()
        self.i = self.i + 1
        self.gridVisual()
        
        print("Step: " + str(self.i))
        print(str(self.score1) + " - " + str(self.score2))
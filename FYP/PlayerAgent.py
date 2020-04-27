# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:40:31 2020

@author: Noel
"""


from mesa import Agent
import numpy as np

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
        self.state = ""
        
        self.shotThreshold = 0.1 #The barrier to taking a shot. Potential to analyse effect of changing threshold
        self.passThreshold = 0.01
        self.passTarget = -1
        self.tackleTarget = -1
        self.stepChoice = ""
 
      
    def checkPossession(self):
        if self.model.newPossession == self.unique_id:
            self.possession = True
            self.model.newPossession = -1
        if (self.possession == True and self.model.newPossession != -1):
            self.possession = False
    
    def checkState(self):
        if self.possession == True:
            if self.goalkeeper == True:
                self.state = "GKP"
            else:
                self.state = "BP"
        else:
            if self.goalkeeper == False:
                changedState = False
                for content, x, y in self.model.grid.coord_iter():
                    if len(content)!=0:
                        for i in content:
                            if (i.possession == True and i.teamID == self.teamID):
                                self.state = "PO"
                                changedState = True
                if changedState == False:
                    self.state = "DF"
            else:
                self.state = "GK"
    
    def choice(self):
        choice = ""
        targetIDs = {}
        if self.possession == True:
            xG = self.shotProb()
            if xG > self.shotThreshold:
                choice = "Shoot"
            else:
                for content, x, y in self.model.grid.coord_iter():
                    if len(content) == 0:
                        pass
                    else:
                        for i in content:
                            if i.teamID == self.teamID:
                                xGTarget = i.shotProb()
                                if xGTarget > xG:
                                    targetIDs[i.unique_id] = xGTarget
                baseVP = 0
                target = -1
                if len(targetIDs) != 0:
                    for key in targetIDs.keys():
                        target = int(key)
                        xP = self.passProb(target)
                        vP = xP*targetIDs[target]
                        if vP > baseVP:
                            baseVP = vP
                if baseVP > self.passThreshold:
                        choice = "Pass"
                        self.passTarget = target
                else:
                    choice = "Move"
        else:
            neighbours = self.model.grid.get_neighborhood(self.pos, moore = True, include_center=True)
            for i in range(len(neighbours)):
                content = self.model.grid.get_cell_list_contents(neighbours[i])
                if len(content) != 0:
                    for i in content:
                        if (i.teamID != self.teamID and i.possession == True):
                            self.tackleTarget = i.unique_id
                            choice = "Tackle"
                        else:
                            choice = "Move"
        return choice
    
    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore = False,
            include_center = False
        )
        movePotentials = []
        for x,y in possibleSteps:
            if self.teamID == 1:
                if self.state == "GK":
                    movePotentials.append(self.model.movePotentialGK1[x][y])
                elif self.state == "GKP":
                    movePotentials.append(self.model.movePotentialGKP1[x][y])
                elif self.state == "DF":
                    movePotentials.append(self.model.movePotentialDF1[x][y])
                elif self.state == "PO":
                    movePotentials.append(self.model.movePotentialPO1[x][y])
                elif self.state == "BP":
                    movePotentials.append(self.model.movePotentialBP1[x][y])
                else:
                    print("Error in move: Player has no state")
            else:
                if self.state == "GK":
                    movePotentials.append(self.model.movePotentialGK2[x][y])
                elif self.state == "GKP":
                    movePotentials.append(self.model.movePotentialGKP2[x][y])
                elif self.state == "DF":
                    movePotentials.append(self.model.movePotentialDF2[x][y])
                elif self.state == "PO":
                    movePotentials.append(self.model.movePotentialPO2[x][y])
                elif self.state == "BP":
                    movePotentials.append(self.model.movePotentialBP2[x][y])
                else:
                    print("Error in move: Player has no state")
        minPotentials = []
        minPotential = movePotentials[0]
        for i in range(len(movePotentials)):
            if movePotentials[i] < minPotential:
                minPotenital = movePotentials[i]
                minPotentials = [i]
            elif movePotentials[i] == minPotential:
                minPotentials.append(i)
        newPosition = possibleSteps[self.model.random.choice(minPotentials)]
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
        
    def shoot(self):
        xG = self.shotProb()
        g = self.model.random.random()
        if xG > g:
            self.possession = False
            if self.teamID == 1:
                self.model.justConceded = 2
            else:
                self.model.justConceded = 1
        else:
            self.possession = False
            for agent, x, y in self.model.grid.coord_iter():
                if len(agent) == 0:
                    pass
                else:
                    for i in agent:
                        if (i.goalkeeper == True and i.teamID != self.teamID):
                            self.model.newPossession = i.unique_id
                        else:
                            pass
    
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
    
    
    def shotProb(self):
        goalStart = (self.model.grid.width/2)-5
        goalEnd = (self.model.grid.width/2)+3
        (x,y) = self.pos
        if self.teamID == 1:
            thetaG2 = np.arctan((goalEnd -x)/(self.model.grid.height-(y)))
            thetaG1 = np.arctan((goalStart -x)/(self.model.grid.height-(y)))
        else:
            thetaG2 = np.arctan((x-goalStart)/(y+1))
            thetaG1 = np.arctan((x-goalEnd)/(y+1))
        thetaG = thetaG2 - thetaG1
        thetaOpen = thetaG
        for cellContent, i, j in self.model.grid.coord_iter():
            if len(cellContent) == 0:
                pass
            else:
                if self.teamID == 1:
                    if j > y:
                        thetaI = np.arctan((i-x)/(j-y))
                        if (thetaI > thetaG1 and thetaI < thetaG2):
                            thetaI2 = np.arctan(((i+1)-x)/((j+1)-y))
                            thetaI1 = np.arctan(((i-1)-x)/((j+1)-y))
                            thetaIt = thetaI2-thetaI1
                        else:
                            thetaIt = 0
                    else:
                        thetaIt = 0
                else:
                    if j < y:
                        thetaI = np.arctan((x-i)/(y-j))
                        if (thetaI > thetaG1 and thetaI < thetaG2):
                            thetaI2 = np.arctan((x-(i-1))/(y-(j-1)))
                            thetaI1 = np.arctan((x-(i+1))/(y-(j-1)))
                            thetaIt = thetaI2-thetaI1
                        else:
                            thetaIt = 0
                    else:
                        thetaIt = 0
                thetaOpen = thetaOpen - thetaIt
        xG = np.sin(thetaOpen/2)-(np.cos(thetaOpen/2)/25)
        return xG
    
    def passProb(self, targetID):
        (x,y) = self.pos
        team = self.teamID
        xTarget = 0
        yTarget = 0
        for agent, i,j in self.model.grid.coord_iter():
            if len(agent) == 0:
                pass
            else:
                for k in agent:
                    if k.unique_id == targetID:
                        xTarget = i
                        yTarget = j
                        r = ((x-i)**2+(y-j)**2)**(0.5)
        rNeighbours = []
        for agent, i, j in self.model.grid.coord_iter():
            if len(agent) == 0:
                pass
            else:
                for k in agent:
                    if k.teamID != team:
                        d = ((xTarget-i)**2+(yTarget-j)**2)**(0.5)
                        if len(rNeighbours) < 3:
                            rNeighbours.append(d)
                        else:
                            for l in range(len(rNeighbours)):
                                if d < rNeighbours[l]:
                                    rNeighbours[l] = d
        avgR = sum(rNeighbours)/len(rNeighbours)
        prob = (avgR/10)*(1-(r/250))
        return prob
    
    def passBall(self, target):
        xP = self.passProb(target)
        p = self.model.random.random()
        if xP > p:
            self.possession = False
            self.model.newPossession = target
        else:
            self.possession = False
            dMin = 10000000
            for content, x, y in self.model.grid.coord_iter():
                if len(content) != 0:
                    for k in content:
                        if k.unique_id == target:
                            i = x
                            j = y
            for content, x, y in self.model.grid.coord_iter():
                if len(content) != 0:
                    for k in content:
                        if k.teamID != self.teamID:
                            d = ((x-i)**2+(y-j)**2)**(0.5)
                            if d < dMin:
                                dMin = d
                                self.model.newPossession = k.unique_id
    
    def tackle(self, target):
        '''
        getNeighborhood
        if ballAgent is in nextCell:
            take possession of ballAgent
        '''
        v = self.model.random.random()
        if v > 0.5:
            self.model.newPossession = self.unique_id
            for content, x, y in self.model.grid.coord_iter():
                if len(content) != 0:
                    for k in content:
                        if k.unique_id == target:
                            k.possession = False
    
    def bugTest(self):
        '''
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
        '''
        if self.possession == True:
            idS = str(self.unique_id)
            print("Unique ID: " + idS)
            xG = str(self.shotProb())
            print("xG: " + xG)
    
    def step(self):
        self.checkPossession()
        self.checkState()
        self.stepChoice = self.choice()
        self.displacement()
        self.avgDisp = self.averageDisp()
        self.maxDisp = self.maxDisplacement()
        self.bugTest()
        
    def advance(self):
        if self.stepChoice == "Shoot":
            self.shoot()
        elif self.stepChoice == "Pass":
            self.passBall(self.passTarget)
        elif self.stepChoice == "Tackle":
            self.tackle(self.tackleTarget)
        else:
            self.move()
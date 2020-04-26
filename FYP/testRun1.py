# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:18:00 2020

@author: Noel
"""


from PitchModel import *
import matplotlib.pyplot as plt

model = PitchModel(11, 68, 100)
for i in range(120):
    model.step()
"""
playerMovement = model.datacollector.get_agent_vars_dataframe()

endMovement = playerMovement.xs(19, level="Step")["Max Displacement"]
plt.figure(1)
plt.clf()
endMovement.hist()
plt.show()

singleMovement = playerMovement.xs(5, level="AgentID")["Avg. Displacement"]
plt.figure(2)
plt.clf()
singleMovement.plot()
plt.show
"""
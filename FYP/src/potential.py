'''
Created on 6 Nov 2019

@author: Noel
'''
import numpy as np

def goalV(x0,y0):
    v = np.zeros((210,136))
    for x in range(210):
        for y in range(136):
            yDiff = y-y0
            if x0 == 0:
                r = np.sqrt((x^2)+(yDiff^2))
            else:
                r = np.sqrt(((210-x)^2)+(yDiff^2))
            if r < 105:
                v[x][y] = r^2
            else:
                v[x][y] = 105^2 + r
    return v

def ballV(x0,y0):
    v = np.zeros((210,136))
    
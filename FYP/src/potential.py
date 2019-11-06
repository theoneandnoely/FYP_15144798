'''
Created on 6 Nov 2019

@author: Noel
'''
import numpy as np

def goalV(x0,y0):
    v = np.zeros((136,210))
    for x in range(210):
        for y in range(136):
            yDiff = y-y0
            if x0 == 0:
                r = np.sqrt((x^2)+(yDiff^2))
            else:
                r = np.sqrt(((210-x)^2)+(yDiff^2))
            if r < 105:
                v[y][x] = r^2
            else:
                v[y][x] = 105^2 + r
    return v

def ballV(x0,y0):
    v = np.zeros((136,210))
    for x in range(210):
        for y in range(136):
            xDiff = x0-x
            yDiff = y0 - y
            r = np.sqrt((xDiff^2)+(yDiff^2))
            v[y][x] = r^2
    return v

def playerV(x0,y0):
    v = np.zeros((136,210))
    v = np.zeros((136,210))
    for x in range(210):
        for y in range(136):
            xDiff = x0-x
            yDiff = y0 - y
            r = np.sqrt((xDiff^2)+(yDiff^2))
            if r > 5:
                v[y][x] = (40)*((10/r)^6-(10/r)^12)+20
            else:
                v[y][x] = 161300
    return v
    
'''
Holds all the dustbin objects and is used for
creation of chromosomes by jumbling their sequence
'''
import numpy as np
import math

class RouteManager:
    destinationDustbins = []
    distanceMatrix = None

    @classmethod
    def addDustbin (cls, db):
        cls.destinationDustbins.append(db)

    @classmethod
    def getDustbin (cls, index):
        return cls.destinationDustbins[index]

    @classmethod
    def numberOfDustbins(cls):
        return len(cls.destinationDustbins)

    @classmethod
    def calculateDistanceMatrix(cls):
        N = cls.numberOfDustbins()
        cls.distanceMatrix = np.zeros((N,N))
        for i in range(N):
            for j in range(i,N):
                dbi = cls.getDustbin(i)
                dbj = cls.getDustbin(j)
                xDis = abs(dbi.getX() - dbj.getX())
                yDis = abs(dbi.getY() - dbj.getY())
                dis = math.sqrt((xDis*xDis) + (yDis*yDis))
                cls.distanceMatrix[i][j] = dis
                cls.distanceMatrix[j][i] = dis


        


"""
Represents nodes in the problem graph or network.
Locatin coordinates can be passed while creating the object or they
will be assigned random values.
"""
import random
import counter
from routemanager import RouteManager
from globals import xMax,yMax

class Dustbin:
    # Good old constructor
    def __init__(self, x=None, y=None, id=-1):
        if x == None and y == None:
            self.x = random.randint(0, xMax)
            self.y = random.randint(0, yMax)
            self.id = -1
        else:
            self.x = x
            self.y = y
            self.id = id

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    # Returns distance to the dustbin passed as argument
    def distanceTo(self, db):
        dis = RouteManager.distanceMatrix[self.id][db.id]
        counter.count = counter.count + 1
        return dis

    # Gives string representation of the Object with coordinates
    def toString(self):
        s = "(" + str(self.getX()) + "," + str(self.getY()) + ")"
        return s

    # Check if cordinates have been assigned or not
    # Dusbins with (-1, -1) as coordinates are created during creation on chromosome objects
    def checkNull(self):
        if self.x == -1:
            return True
        else:
            return False

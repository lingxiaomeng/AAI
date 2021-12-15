"""
Represents the chromosomes in GA's population.
The object is collection of individual routes taken by trucks.
"""
from .routemanager import RouteManager
from .dustbin import Dustbin
from . import globals
import random


class Route:
    # Good old constructor
    def __init__(self, route=None):
        # 2D array which is collection of respective routes taken by trucks
        self.route = []
        # 1D array having routes in a series - used during crossover operation
        self.base = []
        # 1D array having route lengths
        self.routeLengths = self.route_lengths()

        for i in range(globals.numTrucks):
            self.route.append([])

        # fitness value and total distance of all routes
        self.fitness = None
        self.distance = None

        # creating empty route
        if route == None:
            for i in range(RouteManager.numberOfDustbins() - 1):
                self.base.append(Dustbin(-1, -1))

        else:
            self.route = route

    def generateIndividual(self):
        k = 0
        # put 1st member of RouteManager as it is (It represents the initial node) and shuffle the rest before adding
        for dindex in range(1, RouteManager.numberOfDustbins()):
            self.base[dindex - 1] = RouteManager.getDustbin(dindex)
        random.shuffle(self.base)

        for i in range(globals.numTrucks):
            # add same first node for each route
            self.route[i].append(RouteManager.getDustbin(0))
            for j in range(self.routeLengths[i] - 1):
                # add shuffled values for rest
                self.route[i].append(self.base[k])
                k += 1

    # Returns j'th dustbin in i'th route
    def getDustbin(self, i, j):
        return self.route[i][j]

    # Sets value of j'th dustbin in i'th route
    def setDustbin(self, i, j, db):
        self.route[i][j] = db
        # self.route.insert(index, db)
        self.fitness = 0
        self.distance = 0

    # reset distance to 0
    def resetFitness(self):
        self.fitness = None
        self.distance = None

    # Returns the fitness value of route
    def getFitness(self):
        if self.fitness == None:
            self.fitness = 1 / self.getDistance()

        return self.fitness

    # Return total ditance covered in all subroutes
    def getDistance(self):
        if self.distance == None:
            routeDistance = 0

            for i in range(globals.numTrucks):
                for j in range(self.routeLengths[i]):
                    fromDustbin = self.getDustbin(i, j)

                    if j + 1 < self.routeLengths[i]:
                        destinationDustbin = self.getDustbin(i, j + 1)

                    else:
                        destinationDustbin = self.getDustbin(i, 0)

                    routeDistance += fromDustbin.distanceTo(destinationDustbin)

            self.distance = routeDistance
        return self.distance

    # Checks if the route contains a particular dustbin
    def containsDustbin(self, db):
        if db in self.base:  # base <-> route
            return True
        else:
            return False

    # Returns route in the form of a string
    def toString(self):
        geneString = "|"
        print(self.routeLengths)
        # for k in range(RouteManager.numberOfDustbins()-1):
        #    print (self.base[k].toString())
        for i in range(globals.numTrucks):
            for j in range(self.routeLengths[i]):
                geneString += self.getDustbin(i, j).toString() + "|"
            geneString += "\n"

        return geneString

    def visualization(self, plt):
        plt.clf()
        colors = "bgrcmykw"
        for i in range(globals.numTrucks):
            for j in range(self.routeLengths[i]):
                fromDustbin = self.getDustbin(i, j)
                if j + 1 < self.routeLengths[i]:
                    destinationDustbin = self.getDustbin(i, j + 1)
                else:
                    destinationDustbin = self.getDustbin(i, 0)
                sx = fromDustbin.getX()
                sy = fromDustbin.getY()
                ex = destinationDustbin.getX()
                ey = destinationDustbin.getY()
                plt.plot([sx, ex], [sy, ey], colors[i] + ".-")

    @classmethod
    def random_range(cls, n, total):
        """Return a randomly chosen list of n positive integers summing to total.
        Each such list is equally likely to occur."""

        dividers = sorted(random.sample(range(1, total), n - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

    # Randomly distribute number of dustbins to subroutes
    # Maximum and minimum values are maintained to reach optimal result
    @classmethod
    def route_lengths(cls):
        upper = globals.numNodes + globals.numTrucks - 1
        fa = upper / globals.numTrucks * 1.6  # max route length
        fb = upper / globals.numTrucks * 0.6  # min route length
        a = cls.random_range(globals.numTrucks, upper)
        while 1:
            if all(i < fa and i > fb for i in a):
                break
            else:
                a = cls.random_range(globals.numTrucks, upper)
        return a


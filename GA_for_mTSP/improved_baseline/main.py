from .galogic import *
import matplotlib.pyplot as plt
import progressbar
from .dustbin import Dustbin
from . import globals
from . import counter

class ImporvedBaseline:


    @classmethod
    def __init__(cls,numGenerations,plot_progress,seedValue) -> None:
        globals.numGenerations = numGenerations
        globals.plot_progress = plot_progress
        globals.seedValue = seedValue


    @classmethod
    def GA(cls, city):
        globals.numNodes = len(city)
        pbar = progressbar.ProgressBar()

        # Add Dustbins
        for i in range(globals.numNodes):
            RouteManager.addDustbin(Dustbin(city[i][1], city[i][2], i))
        RouteManager.calculateDistanceMatrix()

        random.seed(globals.seedValue)
        yaxis = []  # Fittest value (distance)
        xaxis = []  # Generation count
        counter.count = 0

        pop = Population(globals.populationSize, True)
        globalRoute = pop.getFittest()
        print("Initial minimum distance: " + str(globalRoute.getDistance()))

        # Start evolving
        if globals.plot_progress:
            fig = plt.figure()

        for i in (range(globals.numGenerations)):
            pop = GA.evolvePopulation(pop)
            localRoute = pop.getFittest()
            if globalRoute.getDistance() > localRoute.getDistance():
                globalRoute = localRoute
                if globals.plot_progress:
                    globalRoute.visualization(plt)
                    plt.draw()
                    plt.pause(0.01)
            yaxis.append(localRoute.getDistance())
            xaxis.append(i)

        print(
            "Count: %d Remain steps: %d"
            % (counter.count, globals.numNodes * 20000 - counter.count)
        )

        globalRoute.visualization(plt)
        plt.draw()

        print("Global minimum distance: " + str(globalRoute.getDistance()))
        print("Final Route: " + globalRoute.toString())

        fig = plt.figure()
        plt.plot(xaxis, yaxis, "r-")
        plt.show()
        return globalRoute.getDistance()


from .galogic import *
import matplotlib.pyplot as plt
import progressbar
from .dustbin import Dustbin
from . import globals
from . import counter
from time import process_time


class MultiChromosome :


    @classmethod
    def __init__(cls,numGenerations,plot_progress,seedValue,plot_result:False) -> None:
        globals.numGenerations = numGenerations
        globals.plot_progress = plot_progress
        globals.seedValue = seedValue
        globals.plot_result = plot_result

    @classmethod
    def GA(cls, city):
        globals.numNodes = len(city)
        pbar = progressbar.ProgressBar()
        RouteManager.destinationDustbins = []
        # Add Dustbins
        for i in range(globals.numNodes):
            RouteManager.addDustbin(Dustbin(city[i][1], city[i][2], i))
        RouteManager.calculateDistanceMatrix()

        random.seed(globals.seedValue)
        yaxis = []  # Fittest value (distance)
        xaxis = []  # Generation count
        counter.count = 0
        Population.routes = []

        t_start = process_time()
        pop = Population(globals.populationSize, True)
        globalRoute = pop.getFittest()
        print("Initial minimum distance: " + str(globalRoute.getDistance()))

        # Start evolving
        if globals.plot_progress:
            fig = plt.figure()

        for i in pbar(range(globals.numGenerations)):
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

        t_end = process_time()

        if globals.plot_result:
            plt.figure()
            globalRoute.visualization(plt)
            plt.show()
            plt.figure()
            plt.plot(xaxis, yaxis, "r-")
            plt.show()

        t_cost = t_end - t_start
        return t_cost, globalRoute.getDistance(),counter.count



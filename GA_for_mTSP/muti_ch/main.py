from numpy.core.shape_base import block
from galogic import *
import matplotlib.pyplot as plt
import progressbar
import numpy as np
import counter
from dustbin import Dustbin
from globals import seedValue, populationSize, numGenerations, city, plot_progress

pbar = progressbar.ProgressBar()

# Add Dustbins
for i in range(numNodes):
    RouteManager.addDustbin(Dustbin(city[i][1], city[i][2], i))
RouteManager.calculateDistanceMatrix()


random.seed(seedValue)
yaxis = []  # Fittest value (distance)
xaxis = []  # Generation count
counter.count = 0

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
print("Initial minimum distance: " + str(globalRoute.getDistance()))

# Start evolving
if plot_progress:
    fig = plt.figure()

for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
        if plot_progress:
            globalRoute.visualization(plt)
            plt.draw()
            plt.pause(0.01)
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)

print("Count: %d Remain steps: %d" % (counter.count, numNodes * 20000 - counter.count))

globalRoute.visualization(plt)
plt.draw()

print("Global minimum distance: " + str(globalRoute.getDistance()))
print("Final Route: " + globalRoute.toString())

fig = plt.figure()

plt.plot(xaxis, yaxis, "r-")
plt.show()

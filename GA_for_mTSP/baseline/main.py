from numpy.core.shape_base import block
from galogic import *
import matplotlib.pyplot as plt
import progressbar
import numpy as np
import counter

pbar = progressbar.ProgressBar()

city_path = "/home/mlx/AAI/instances/mtsp51.txt"
# Add Dustbins
city = np.genfromtxt(city_path, dtype=int, skip_header=1)
numNodes = len(city)

for i in range(numNodes):
    RouteManager.addDustbin(Dustbin(city[i][1], city[i][2]))

random.seed(seedValue)
yaxis = []  # Fittest value (distance)
xaxis = []  # Generation count

Population.routes = []
pop = Population(populationSize, True)
globalRoute = pop.getFittest()
print("Initial minimum distance: " + str(globalRoute.getDistance()))

# Start evolving
# fig = plt.figure()

counter.count = 0
for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
        # globalRoute.visualization(plt)
        # plt.draw()
        # plt.pause(0.01)
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)

print("Count: %d Remain steps: %d"%(counter.count, numNodes*20000 - counter.count))

globalRoute.visualization(plt)
plt.draw()

print("Global minimum distance: " + str(globalRoute.getDistance()))
print("Final Route: " + globalRoute.toString())

fig = plt.figure()

plt.plot(xaxis, yaxis, "r-")
plt.show()

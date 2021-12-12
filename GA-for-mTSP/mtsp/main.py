from galogic import *
import matplotlib.pyplot as plt
import progressbar
import numpy as np

pbar = progressbar.ProgressBar()

city_path = "/home/mlx/AAI/instances/mtsp51.txt"
# Add Dustbins
city = np.genfromtxt(city_path, dtype=int,skip_header = 1)
numNodes = len(city)

for i in range(numNodes):
    RouteManager.addDustbin(Dustbin(city[i][1], city[i][2]))

random.seed(seedValue)
yaxis = [] # Fittest value (distance)
xaxis = [] # Generation count

pop = Population(populationSize, True)
globalRoute = pop.getFittest()
print ('Initial minimum distance: ' + str(globalRoute.getDistance()))

# Start evolving
fig = plt.figure()
for i in pbar(range(numGenerations)):
    pop = GA.evolvePopulation(pop)
    localRoute = pop.getFittest()
    if globalRoute.getDistance() > localRoute.getDistance():
        globalRoute = localRoute
        # print(globalRoute.toString())
        globalRoute.visualization(plt)
        plt.draw()
    yaxis.append(localRoute.getDistance())
    xaxis.append(i)

print ('Global minimum distance: ' + str(globalRoute.getDistance()))
print ('Final Route: ' + globalRoute.toString())

fig = plt.figure()

plt.plot(xaxis, yaxis, 'r-')
plt.show()

import numpy as np
import random


route = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25],
]

indexs = np.random.permutation(5)
indexs = indexs[0:random.randint(1,5)]
print(indexs)

toslide = route[indexs[0]][-1]
for k in range(1,len(indexs)):
    tempgen = route[indexs[k]][-1]
    route[indexs[k]][1:] = route[indexs[k]][0:-1]
    route[indexs[k]][0] = toslide
    toslide = tempgen
route[indexs[0]][1:] = route[indexs[0]][0:-1]
route[indexs[0]][0] = toslide

print(route)

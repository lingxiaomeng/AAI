a = [1,2,3,4,5]
b = [6,7,8,9,10]

route1startPos = 1
route1lastPos = 2

route2startPos = 1
route2lastPos = 2

swap1 =a[route1startPos:route1startPos]  # values from 1
swap1.reverse()
# add to new location by pushing
a[route1startPos:route1startPos] = swap1


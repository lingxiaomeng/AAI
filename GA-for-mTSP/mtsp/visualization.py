import matplotlib.pyplot as plt


def show_route(route):
    geneString = '|'
    print(route.routeLengths)
    # for k in range(RouteManager.numberOfDustbins()-1):
    #    print (self.base[k].toString())
    for i in range(numTrucks):
        for j in range(self.routeLengths[i]):
            geneString += self.getDustbin(i, j).toString() + '|'
        geneString += '\n'

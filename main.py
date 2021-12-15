import numpy as np
from GA_for_mTSP.improved_baseline.main import ImporvedBaseline
city_path = "./instances/mtsp51.txt"
city = np.genfromtxt(city_path, dtype=int, skip_header=1)
d = []

imporved_baseline = ImporvedBaseline(numGenerations=100,plot_progress=False,seedValue=0)
imporved_baseline.GA(city=city)

imporved_baseline = ImporvedBaseline(numGenerations=100,plot_progress=False,seedValue=1)
imporved_baseline.GA(city=city)
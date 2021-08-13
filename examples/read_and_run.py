from oopnet.api import *
import os

filename = os.path.join('data', 'Poulakis.inp')

network = Read(filename)

for j in network.junctions:
    print(j, j.demand, j.elevation)

report = Run(network)
print(report)

p = Pressure(report)
print(p)
print(p.describe())

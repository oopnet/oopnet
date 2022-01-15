import os

from oopnet import *

filename = os.path.join('data', 'Poulakis.inp')

network = Read(filename)

for j in get_junctions(network):
    print(j, j.demand, j.elevation)

report = Run(network, delete=False)
print(report)

p = Pressure(report)
print(p)
print(p.describe())

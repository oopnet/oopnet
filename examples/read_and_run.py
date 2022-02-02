import os

import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')

network = on.Read(filename)

for j in on.get_junctions(network):
    print(j, j.demand, j.elevation)

report = on.Run(network, delete=False)
print(report)

p = on.Pressure(report)
print(p)
print(p.describe())

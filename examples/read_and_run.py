import os

import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')

network = on.Network.read(filename)

for j in on.get_junctions(network):
    print(j, j.demand, j.elevation)

report = network.run()
print(report)

p = report.pressure
print(p)
print(p.describe())

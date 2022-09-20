import os

import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')
network = on.Network.read(filename)

print(network.options.demandmodel)
print(network.times.duration)

network.reportparameter.velocity = 'NO'
network.reportparameter.length = 'YES'

network.reportprecision.flow = 3

import os
from datetime import timedelta

from matplotlib import pyplot as plt
import numpy as np
import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')

network = on.Network.read(filename)

pat1 = on.Pattern(id='1', multipliers=list(np.linspace(0.5, 1.5, 10)))
on.add_pattern(network, pat1)
# network.patterns = [pat1]

for j in on.get_junctions(network):
    j.demandpattern = pat1
network.times.duration = timedelta(hours=18)


report = network.run()

# todo: enable after fixing linkinfo
#on.Linkinfo(report, linkname='P-03').plot()
plt.show()


# ax = plt.subplot(111)


# Pressure(report).plot(ax=ax)
# Flow(report).plot(ax=ax)
# Show()

# Pressure(report)['J-03', 'J-05'].plot()


# Show()
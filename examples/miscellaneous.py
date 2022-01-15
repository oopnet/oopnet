import os

from oopnet import *
from oopnet.elements import Pattern

filename = os.path.join('data', 'Poulakis.inp')

network = Read(filename)

pat1 = Pattern(id='1', multipliers=list(np.linspace(0.5, 1.5, 10)))
add_pattern(network, pat1)
# network.patterns = [pat1]

for j in get_junctions(network):
    j.demandpattern = pat1
network.times.duration = timedelta(hours=18)


report = Run(network)

Linkinfo(report, linkname='P-03').plot()
plt.show()


# ax = plt.subplot(111)


# Pressure(report).plot(ax=ax)
# Flow(report).plot(ax=ax)
# Show()

# Pressure(report)['J-03', 'J-05'].plot()


# Show()
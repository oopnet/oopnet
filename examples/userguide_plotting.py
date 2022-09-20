import os

from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Network.read(filename)

net.plot()

rpt = net.run()
p = rpt.pressure
f = rpt.flow

net.plot(nodes=p, links=f)
net.plot(nodes=p, links=f, robust=True)

p_reduced = p.iloc[:50]
net.plot(nodes=p_reduced, links=f, robust=True, truncate_nodes=True)

diameters = on.get_diameter(net)
net.plot(linkwidth=diameters, links=f, markersize=0)

plt.show()

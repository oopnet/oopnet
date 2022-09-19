import os

from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Network.read(filename)

net.plot()

rpt = net.run()
p = rpt.pressure
f = rpt.flow

net.plot(nodes=p, links=f, fignum=1)
net.plot(nodes=p, links=f, fignum=2, robust=True)

p_reduced = p.iloc[:50]
net.plot(nodes=p_reduced, links=f, fignum=3, robust=True, truncate_nodes=True)

diameters = on.get_diameter(net)
net.plot(linkwidth=diameters, markersize=0, fignum=4)

plt.show()


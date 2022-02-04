import os

from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Network.read(filename)
rpt = net.run()

p = rpt.pressure
f = rpt.flow

net.plot(nodes=p, links=f, fignum=1)

net.plot(nodes=p, links=f, fignum=2, robust=True)
plt.show()


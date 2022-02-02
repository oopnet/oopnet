import os

from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Network.read(filename)
rpt = net.run()

p = on.Pressure(rpt)
f = on.Flow(rpt)

on.Plot(net, nodes=p, links=f, fignum=1)

on.Plot(net, nodes=p, links=f, fignum=2, robust=True)
plt.show()

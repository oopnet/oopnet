import os

from oopnet import *

filename = os.path.join('data', 'C-town.inp')

net = Read(filename)
rpt = Run(net)

p = Pressure(rpt)
f = Flow(rpt)

Plot(net, nodes=p, links=f, fignum=1)

Plot(net, nodes=p, links=f, fignum=2, robust=True)
plt.show()

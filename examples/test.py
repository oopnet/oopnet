import os

from oopnet import *

filename = os.path.join('data', 'anytown.inp')

net = Read(filename)
net.report.nodes = 'ALL'
net.report.links = 'ALL'
rpt = Run(net)
print(net.reportparameter.pressure)
p = Pressure(rpt)
Plot(net, nodes=p['1'])
plt.show()

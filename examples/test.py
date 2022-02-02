import os

from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'anytown.inp')

net = on.Read(filename)
net.report.nodes = 'ALL'
net.report.links = 'ALL'
rpt = on.Run(net)
print(net.reportparameter.pressure)
p = on.Pressure(rpt)
on.Plot(net, nodes=p['1'])
plt.show()

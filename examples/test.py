import os

from oopnet.api import *

# todo: fix

filename = os.path.join('data', 'anytown.inp')

net = Read(filename)
net.report.nodes = 'ALL'
net.report.links = 'ALL'
rpt = Run(net)

Plot(net, nodes=Pressure(rpt))
Show()

import os
from datetime import timedelta

from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter

import oopnet as on
from oopnet.plotter.pyplot import NetworkPlotter

filename = os.path.join('data', 'L-L-TOWN_AreaC.inp')

net = on.Network.read(filename)
net.times.reporttimestep = timedelta(hours=1)
rpt = net.run()

p = rpt.pressure
f = rpt.flow

fig, ax = plt.subplots(figsize=(15, 10))
anim = NetworkPlotter(robust=True).animate(net, ax=ax, nodes=p.abs(), links=f.abs(), node_label="Pressure (m)", link_label="Flow (m)", interval=300)
anim.save("simple_animation.gif", dpi=300, writer=PillowWriter(fps=10))
plt.show()

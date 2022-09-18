import os

from matplotlib import pyplot as plt
from matplotlib.animation import PillowWriter

import oopnet as on

filename = os.path.join('data', 'L-TOWN_AreaC.inp')
net = on.Network.read(filename)

rpt = net.run()

p = rpt.pressure.loc['2016-01-01']
f = rpt.flow.loc['2016-01-01']
print(p)
print(f)

fig, ax = plt.subplots(figsize=(7.5, 5))
anim = net.animate(ax=ax, nodes=p, links=f.abs(), node_label="Pressure (m)", link_label="Flow (m)", robust=True, interval=50)
anim.save("simple_animation.gif", dpi=200, writer=PillowWriter(fps=20))

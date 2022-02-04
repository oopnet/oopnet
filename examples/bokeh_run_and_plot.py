import os

from bokeh.plotting import output_file, show
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Network.read(filename)
rpt = net.run()

p = rpt.pressure
f = rpt.flow

output_file('bokehexample.html')
plot = net.bokehplot(nodes=p, links=f, colormap=dict(node='viridis', link='cool'))
show(plot)

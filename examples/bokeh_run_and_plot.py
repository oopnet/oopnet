import os

from bokeh.plotting import output_file, show
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Read(filename)
rpt = on.Run(net)

p = on.Pressure(rpt)
f = on.Flow(rpt)

output_file('bokehexample.html')
p = on.BPlot(net, nodes=p, links=f, colormap=dict(node='viridis', link='cool'))
show(p)

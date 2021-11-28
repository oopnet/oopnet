import os

import networkx as nx

from oopnet.api import *

# todo: checks examples in docs (line numbers etc.)


filename = os.path.join('..', 'examples', 'data', 'Poulakis.inp')

net = Read(filename)

add_junction(network=net, id='J-32', xcoordinate=5500, ycoordinate=8000, demand=80)

add_pipe(network=net, id='P-51', length=1000, diameter=400, roughness=0.26, startnode=get_node(net, 'J-32'),
         endnode=get_node(net, 'J-26'))

rjid = 'J-24'
G = MultiGraph(network=net)
nn = nx.neighbors(G, rjid)

for neighbour in nn:
    np = G.get_edge_data(u=neighbour, v=rjid)[0]
    npid = np['id']
    remove_pipe(network=net, id=npid)

remove_junction(network=net, id=rjid)

add_pipe(network=net, id='P-52', length=2000, diameter=400, roughness=0.26, startnode=get_node(net, 'J-23'),
         endnode=get_node(net, 'J-25'))

add_reservoir(network=net, id='J-53', head=2, xcoordinate=5500, ycoordinate=4500)

add_pump(network=net, id='Pump1', keyword='POWER', value=50, startnode=get_node(net, 'J-53'),
         endnode=get_node(net, 'J-31'))

rpt = Run(net, output=True)
Plot(net, links=Flow(rpt), nodes=Pressure(rpt), robust=True)

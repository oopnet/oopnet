from oopnet.api import *
import os
import networkx as nx

filename = os.path.join('..', 'examples', 'data', 'Poulakis.inp')

net = Read(filename)

add_junction(network=net, id='J-32', xcoordinate=5500, ycoordinate=8000, demand=80)

add_pipe(network=net, id='P-51', length=1000, diameter=400, roughness=0.26, startnodeid='J-32', endnodeid='J-26')

rjid = 'J-24'
G = MultiGraph(network=net)
nn = nx.neighbors(G, rjid)

for neighbour in nn:
    np = G.get_edge_data(u=neighbour, v=rjid)[0]
    npid = np['id']
    remove_pipe(network=net, id=npid)

remove_junction(network=net, id=rjid)

add_pipe(network=net, id='P-52', length=2000, diameter=400, roughness=0.26, startnodeid='J-23', endnodeid='J-25')

add_reservoir(network=net, id='J-53', head=2, xcoordinate=5500, ycoordinate=4500)

add_pump(network=net, id='Pump1', keyword='POWER', value=50, startnodeid='J-53', endnodeid='J-31')

rpt = Run(net)
Plot(net, links=Flow(rpt), nodes=Pressure(rpt), robust=True)

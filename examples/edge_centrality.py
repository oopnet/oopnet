from oopnet.api import *
from oopnet.graph.graph import edgeresult2pandas
import os
import networkx as nx

filename = os.path.join('..', 'examples', 'data', 'anytown.inp')

net = Read(filename)

G = Graph(net)

c = nx.edge_betweenness_centrality(G)

c = edgeresult2pandas(G, c)
c.name = 'Edge-betweenness Centrality'

Plot(net, links=c)
Show()
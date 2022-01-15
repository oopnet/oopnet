import os

import networkx as nx

from oopnet import *

filename = os.path.join('data', 'anytown.inp')

net = Read(filename)

G = MultiGraph(net)

c = nx.edge_betweenness_centrality(G)

c = edgeresult2pandas(G, c)
c.name = 'Edge-betweenness Centrality'
print(c)
Plot(net, links=c)
plt.show()

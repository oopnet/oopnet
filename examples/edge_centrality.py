import os

import networkx as nx
from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'anytown.inp')

net = on.Read(filename)

G = on.MultiGraph(net)

c = nx.edge_betweenness_centrality(G)

c = on.edgeresult2pandas(G, c)
c.name = 'Edge-betweenness Centrality'
print(c)
on.Plot(net, links=c)
plt.show()

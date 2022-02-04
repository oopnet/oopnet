import os

import networkx as nx
from matplotlib import pyplot as plt
import oopnet as on

filename = os.path.join('data', 'anytown.inp')

net = on.Network.read(filename)

G = on.MultiGraph(net)

c = nx.edge_betweenness_centrality(G)

c = on.edgeresult2pandas(G, c)
c.name = 'Edge-betweenness Centrality'
print(c)
net.plot(links=c)
plt.show()

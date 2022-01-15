import os

import networkx as nx

from oopnet import *

filename = os.path.join('data', 'C-town.inp')

net = Read(filename)

G = Graph(net)

plt.figure()

dc = nx.degree_centrality(G)
dc = pd.Series(dc)
dc.name = 'Degree Centrality'
ax = plt.subplot(221)
Plot(net, nodes=dc, ax=ax)

cc = nx.closeness_centrality(G)
cc = pd.Series(cc)
cc.name = 'Closeness Centrality'
ax = plt.subplot(222)
Plot(net, nodes=cc, ax=ax)

bc = nx.betweenness_centrality(G)
bc = pd.Series(bc)
bc.name = 'Betweenness Centrality'
ax = plt.subplot(223)
Plot(net, nodes=bc, ax=ax)

cfcc = nx.current_flow_closeness_centrality(G)
cfcc = pd.Series(cfcc)
cfcc.name = 'Current Flow Closeness Centrality'
ax = plt.subplot(224)
Plot(net, nodes=cfcc, ax=ax)

lc = nx.load_centrality(G)
lc = pd.Series(lc)
lc.name = 'Load Centrality'
Plot(net, nodes=lc)

plt.show()

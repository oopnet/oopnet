import os

import networkx as nx

from oopnet.api import *

# todo: fix
filename = os.path.join('..', 'examples', 'data', 'C-town.inp')

net = Read(filename)

G = Graph(net)

plt.figure(1)
ax = plt.subplot(221)

dc = nx.degree_centrality(G)
dc = pd.Series(dc)
dc.name = 'Degree Centrality'
Plot(net, nodes=dc, ax=ax)

ax = plt.subplot(222)
cc = nx.closeness_centrality(G)
cc = pd.Series(cc)
cc.name = 'Closeness Centrality'
Plot(net, nodes=cc, ax=ax)

ax = plt.subplot(223)
bc = nx.betweenness_centrality(G)
bc = pd.Series(bc)
bc.name = 'Betweenness Centrality'
Plot(net, nodes=bc, ax=ax)

ax = plt.subplot(224)
cfcc = nx.current_flow_closeness_centrality(G)
cfcc = pd.Series(cfcc)
cfcc.name = 'Current Flow Closeness Centrality'
Plot(net, nodes=cfcc, ax=ax)

lc = nx.load_centrality(G)
lc = pd.Series(lc)
lc.name = 'Load Centrality'
Plot(net, nodes=lc)

Show()
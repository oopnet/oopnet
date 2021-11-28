import os

import networkx as nx

from oopnet.api import *

# Read file into OOPNET
filename = os.path.join('data', 'anytown.inp')
network = Read(filename)

# Save graph to variable G
G = Graph(network)
print(type(G))

# Some graph theoretic measurements:
print('Center:', nx.center(G))
print('Diameter:', nx.diameter(G))
print('Radius:', nx.radius(G))

# Page Rank algorithm
pr = nx.pagerank_numpy(G)
pr = pd.Series(pr)
pr.sort_values(ascending=False, inplace=True)
pr.name = 'Page Rank'

# Barplot
f, ax = plt.subplots()
pr.plot(kind='bar', ax=ax)

# Plot PageRank in network
Plot(network, nodes=pr)

# Histogram of degrees in the network
deg = nx.degree_histogram(G)
deg = pd.Series(deg)

f, ax = plt.subplots()
deg.plot(kind='bar', ax=ax)
plt.xlabel('degree', fontsize=16)
plt.ylabel('frequency', fontsize=16)

# Calculate all shortest paths:
paths = nx.all_pairs_dijkstra_path_length(G)
df = pd.DataFrame(paths)

# Plot shortest paths between all nodes
f, ax = plt.subplots()
# todo: fix
sns.heatmap(df, square=True, xticklabels=5, yticklabels=5, linewidths=.5)
Show()

import os

import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import oopnet as on

filename = os.path.join('data', 'anytown.inp')
network = on.Network.read(filename)

G = on.MultiGraph(network)

print(f'Center: {nx.center(G)}')
print(f'Diameter: {nx.diameter(G)}')
print(f'Radius: {nx.radius(G)}')

pr = nx.pagerank(G)
pr = pd.Series(pr)
pr.sort_values(ascending=False, inplace=True)
pr.name = 'Page Rank'

f, ax = plt.subplots()
pr.plot(kind='bar', ax=ax)

network.plot(nodes=pr)

deg = nx.degree_histogram(G)
deg = pd.Series(deg)

f, ax = plt.subplots()
deg.plot(kind='bar', ax=ax)
plt.xlabel('degree', fontsize=16)
plt.ylabel('frequency', fontsize=16)
paths = dict(nx.all_pairs_dijkstra_path_length(G))
df = pd.DataFrame(paths)

f, ax = plt.subplots()
sns.heatmap(df, square=True, xticklabels=5, yticklabels=5, linewidths=.5)
plt.show()

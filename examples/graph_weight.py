import os

import networkx as nx
import oopnet as on

filename = os.path.join('data', 'C-town.inp')

net = on.Network.read(filename)

G = on.MultiGraph(net)
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

G = on.MultiGraph(net, weight='diameter')
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

G = on.MultiGraph(net, weight='diameter', default=0)
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

import os

import networkx as nx
import oopnet as on

# todo: fix

filename = os.path.join('data', 'C-town.inp')

net = on.Read(filename)

G = on.Graph(net, weight='diameter')
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

G = on.Graph(net, weight='diameter', default=0)
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

G = on.Graph(net, weight='length', default=0)
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

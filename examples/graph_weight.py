import os

import networkx as nx

from oopnet import *

# todo: fix

filename = os.path.join('data', 'C-town.inp')

net = Read(filename)

G = Graph(net, weight='diameter')
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

G = Graph(net, weight='diameter', default=0)
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

G = Graph(net, weight='length', default=0)
avg_sp = nx.average_shortest_path_length(G, 'weight')
print(f'Average Shortest Path: {avg_sp}')

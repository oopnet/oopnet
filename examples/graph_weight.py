from oopnet.api import *
import os
import networkx as nx

filename = os.path.join('..', 'examples', 'data', 'C-town.inp')

net = Read(filename)

G = Graph(net, weight='diameter', default=None)

print(nx.average_shortest_path_length(G, 'weight'))

G = Graph(net, weight='diameter', default=0)

print(nx.average_shortest_path_length(G, 'weight'))

G = Graph(net, weight='length', default=0)

print(nx.average_shortest_path_length(G, 'weight'))
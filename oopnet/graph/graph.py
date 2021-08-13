import networkx as nx
import pandas as pd
from ..utils.getters.element_lists import get_node_ids, get_links


def graph(network, weight='length', default=0.00001):
    """
    This function generates an undirected NetworkX graph from an OOPNET network
    :param network: OOPNET network object
    :param weight: name of pipe property as a string which is used as weight
    :param default: When a default argument is given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.
    :return: undirected graph (networkx.Graph()-object)
    """

    g = nx.Graph()

    for n in get_node_ids(network):
        g.add_node(n)

    for l in get_links(network):
        e = (l.startnode.id,
             l.endnode.id)
        if l in network.pipes:
            length = getattr(l, weight, default)
        else:
            length = 0.0
        lid = l.id

        g.add_edge(*e, weight=length, id=lid)

    if network.pumps:
        for p in network.pumps:
            g.get_edge_data(p.startnode.id, p.endnode.id)[0]['weight'] = 0.00001

    if network.valves:
        for v in network.valves:
            g.get_edge_data(v.startnode.id, v.endnode.id)[0]['weight'] = 0.00001

    return g


def digraph(network, weight='length', default=0.00001):
    """
    This function generates an directed NetworkX graph from an OOPNET network
    :param network: OOPNET network object
    :param weight: name of pipe property as a string which is used as weight
    :param default: When a default argument is given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.
    :return: directed graph (networkx.DiGraph()-object)
    """

    g = nx.DiGraph()

    for n in get_node_ids(network):
        g.add_node(n)

    for l in get_links(network):
        e = (l.startnode.id,
             l.endnode.id)
        if l in network.pipes:
            length = getattr(l, weight, default)
        else:
            length = 0.0
        lid = l.id

        g.add_edge(*e, weight=length, id=lid)

    if network.pumps:
        for p in network.pumps:
            g.get_edge_data(p.startnode.id, p.endnode.id)[0]['weight'] = 0.00001

    if network.valves:
        for v in network.valves:
            g.get_edge_data(v.startnode.id, v.endnode.id)[0]['weight'] = 0.00001

    return g


def multigraph(network, weight='length', default=0.00001):
    """
    This function generates an undirected NetworkX graph from an OOPNET network
    :param network: OOPNET network object
    :param weight: name of pipe property as a string which is used as weight
    :param default: When a default argument is given, it is returned when the attribute doesn't
    exist; without it, an exception is raised in that case.
    :return: undirected graph (networkx.Graph()-object)
    """
    g = nx.MultiGraph()

    for n in get_node_ids(network):
        g.add_node(n)

    for l in get_links(network):
        e = (l.startnode.id,
             l.endnode.id)
        if l in network.pipes:
            length = getattr(l, weight, default)
        else:
            length = 0.0
        lid = l.id

        g.add_edge(*e, weight=length, id=lid)

    if network.pumps:
        for p in network.pumps:
            g.get_edge_data(p.startnode.id, p.endnode.id)[0]['weight'] = 0.00001

    if network.valves:
        for v in network.valves:
            g.get_edge_data(v.startnode.id, v.endnode.id)[0]['weight'] = 0.00001

    return g


def onlinks2nxlinks(network):
    edges = []
    for l in network.pipes:
        edges.append((l.startnode.id, l.endnode.id))
    return edges


def nxlinks2onlinks(G):

    pipelist = []
    for n1, n2 in G.edges():
        pipelist.append(G.get_edge_data(n1, n2)['id'])
    return pipelist


def edge2pipeid(G, edge):

    return G.get_edge_data(edge[0], edge[1])['id']


def edgeresult2pandas(G, result):
    """
    Transform edge data retrieved e.g. from edge centric centrality measurements to a Pandas Series compatible with OOPNET
    :param G: networkx graph object
    :param result: dictionary with nodeduple as keys
    :return: transformed result into a pandas series
    """
    for edge in list(result.keys()):
        pipe = edge2pipeid(G, edge)
        result[pipe] = result.pop(edge)
    return pd.Series(result)


# class Graph(HasStrictTraits):
#
#     def __init__(self, network):
#         super(Graph, self).__init__()
#
#         g = nx.Graph()
#
#         for n in get_node_ids(network):
#             g.add_node(n)
#
#         if network.pipes:
#             for p in network.pipes:
#                 e = (p.startnode.id, p.endnode.id, {'weight': p.length, 'id': p.id})
#                 g.add_edge(*e)
#
#         if network.valves:
#             for p in network.valves:
#                 e = (p.startnode.id, p.endnode.id, {'weight': length(p), 'id': p.id})
#                 g.add_edge(*e)
#
#         if network.pumps:
#             for p in network.pumps:
#                 e = (p.startnode.id, p.endnode.id, {'weight': length(p), 'id': p.id})
#                 g.add_edge(*e)
#
#         network.graph = g
#
#
# class DiGraph(HasStrictTraits):
#
#     def __init__(self, network):
#         super(DiGraph, self).__init__()
#
#         g = nx.DiGraph()
#
#         for j in network.junctions:
#             g.add_node(j.id)
#
#         for p in network.pipes:
#             e = (p.startnode.id, p.endnode.id, {'weight': p.length, 'id': p.id})
#             g.add_edge(*e)
#
#         if network.valves:
#             for p in network.valves:
#                 e = (p.startnode.id, p.endnode.id, {'weight': length(p), 'id': p.id})
#                 g.add_edge(*e)
#
#         if network.pumps:
#             for p in network.pumps:
#                 e = (p.startnode.id, p.endnode.id, {'weight': length(p), 'id': p.id})
#                 g.add_edge(*e)
#
#         network.graph = g
#
#
# class FlowDiGraph(HasStrictTraits):
#
#     def __init__(self, network):
#         super(FlowDiGraph, self).__init__()
#         g = nx.DiGraph()
#
#         rpt = Run(network)
#         flows = rpt.pivot_table('Flow', index='id').abs().dropna()
#         for j in network.junctions:
#             g.add_node(j.id)
#
#         for p in network.pipes:
#
#             if flows[p.id] >= 0.0:
#                 e = (p.startnode.id, p.endnode.id, {'weight': p.length, 'id': p.id})
#             else:
#                 e = (p.endnode.id, p.startnode.id, {'weight': p.length, 'id': p.id})
#
#             g.add_edge(*e)
#
#         network.graph = g

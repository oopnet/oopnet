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
        length = getattr(l, weight, default) if l in network.pipes else 0.0
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
        length = getattr(l, weight, default) if l in network.pipes else 0.0
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
        length = getattr(l, weight, default) if l in network.pipes else 0.0
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
    return [(l.startnode.id, l.endnode.id) for l in network.pipes]


def nxlinks2onlinks(G):
    return [G.get_edge_data(n1, n2)['id'] for n1, n2 in G.edges()]


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

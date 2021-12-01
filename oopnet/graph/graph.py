import networkx as nx
import pandas as pd

from oopnet.utils.getters.element_lists import get_node_ids, get_links, get_pumps, get_valves, get_pipes
from oopnet.elements.network import Network


def graph(network: Network, weight: str = 'length', default: float = 0.00001) -> nx.Graph:
    """This function generates an undirected NetworkX graph from an OOPNET network

    Args:
      network: OOPNET network object
      weight: name of pipe property as a string which is used as weight (Default value = 'length')
      default: When a default argument is given, it is returned when the attribute doesn't exist; without it, an exception is raised in that case. (Default value = 0.00001)

    Returns:
      undirected graph
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

    for p in get_pumps(network):
        g.get_edge_data(p.startnode.id, p.endnode.id)['weight'] = 0.00001

    for v in get_valves(network):
        g.get_edge_data(v.startnode.id, v.endnode.id)[0]['weight'] = 0.00001

    return g


def digraph(network: Network, weight: str = 'length', default: float = 0.00001) -> nx.DiGraph:
    """This function generates an directed NetworkX graph from an OOPNET network

    Args:
      network: OOPNET network object
      weight: name of pipe property as a string which is used as weight (Default value = 'length')
      default: When a default argument is given, it is returned when the attribute doesn't exist; without it, an exception is raised in that case. (Default value = 0.00001)

    Returns:
      directed graph
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

    for p in get_pumps(network):
        g.get_edge_data(p.startnode.id, p.endnode.id)[0]['weight'] = 0.00001

    for v in get_valves(network):
        g.get_edge_data(v.startnode.id, v.endnode.id)[0]['weight'] = 0.00001

    return g


def multigraph(network: Network, weight: str = 'length', default: float = 0.00001) -> nx.MultiGraph:
    """This function generates an undirected NetworkX graph from an OOPNET network

    Args:
      network: OOPNET network object
      weight: name of pipe property as a string which is used as weight (Default value = 'length')
      default: When a default argument is given, it is returned when the attribute doesn't exist; without it, an exception is raised in that case. (Default value = 0.00001)

    Returns:
      undirected graph
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

    for p in get_pumps(network):
        g.get_edge_data(p.startnode.id, p.endnode.id)[0]['weight'] = 0.00001

    for v in get_valves(network):
        g.get_edge_data(v.startnode.id, v.endnode.id)[0]['weight'] = 0.00001

    return g


def onlinks2nxlinks(network: Network) -> list:
    """
    Args:
      network:

    Returns:

    """
    return [(l.startnode.id, l.endnode.id) for l in get_pipes(network)]


def nxlinks2onlinks(G: nx.Graph) -> list:
    """

    Args:
      G:

    Returns:

    """
    return [G.get_edge_data(n1, n2)['id'] for n1, n2 in G.edges()]


def edge2pipeid(G: nx.Graph, edge: dict) -> dict:
    """

    Args:
      G:
      edge:

    Returns:

    """
    return G.get_edge_data(edge[0], edge[1])['id']


def edgeresult2pandas(G: nx.Graph, result: dict) -> pd.Series:
    """Transform edge data retrieved e.g. from edge centric centrality measurements to a Pandas Series compatible with OOPNET

    Args:
      G: networkx graph object
      result: dictionary with nodeduple as keys

    Returns:
      transformed result into a pandas series
    """
    for edge in list(result.keys()):
        pipe = edge2pipeid(G, edge)
        result[pipe] = result.pop(edge)
    return pd.Series(result)

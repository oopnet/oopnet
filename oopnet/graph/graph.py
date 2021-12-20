import networkx as nx
import pandas as pd

from oopnet.utils.getters.element_lists import get_node_ids, get_links, get_pipes
from oopnet.elements.network import Network


# todo: add report weights (e.g., flow, headloss)
def _add_nodes(graph, network):
    graph.add_nodes_from(get_node_ids(network))


def _add_links(graph, network, weight, default):
    for l in get_links(network):
        e = (l.startnode.id,
             l.endnode.id)
        weight_value = getattr(l, weight, default)
        graph.add_edge(*e, weight=weight_value, id=l.id)


def graph(network: Network, weight: str = 'length', default: float = 0.00001) -> nx.Graph:
    """This function generates an undirected NetworkX graph from an OOPNET network

    Args:
      network: OOPNET network object
      weight: name of pipe property as a string which is used as weight (Default value = 'length')
      default: When set, the default value is returned as weight for objects that don't have the defined weight attribute. Without it, an exception is raised for those objects. (Default value = 0.00001)

    Returns:
      undirected graph
    """
    g = nx.Graph()
    _add_nodes(g, network)
    _add_links(g, network, weight, default)
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
    _add_nodes(g, network)
    _add_links(g, network, weight, default)
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
    _add_nodes(g, network)
    _add_links(g, network, weight, default)
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

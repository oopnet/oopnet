import networkx as nx
import pandas as pd

from oopnet.utils.getters.element_lists import get_node_ids, get_links, get_pumps, get_valves, get_pipes
from oopnet.elements.network import Network

def _add_graph_components(graph, network, weight, default):
    for n in get_node_ids(network):
        graph.add_node(n)

    pipes = get_pipes(network)
    for l in get_links(network):
        e = (l.startnode.id,
             l.endnode.id)
        weight_value = getattr(l, weight, default) if l in pipes else 0.00001
        graph.add_edge(*e, weight=weight_value, id=l.id)

    return graph


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
    return _add_graph_components(g, network, weight, default)


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
    return _add_graph_components(g, network, weight, default)


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
    return _add_graph_components(g, network, weight, default)


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

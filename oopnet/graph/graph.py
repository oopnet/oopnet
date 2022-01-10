from __future__ import annotations
from typing import TYPE_CHECKING, Union

import networkx as nx
import pandas as pd

from oopnet.utils.getters import get_node_ids, get_links, get_pipes
if TYPE_CHECKING:
    from oopnet.elements import Network


# todo: add documentation
def _add_nodes(graph, network):
    graph.add_nodes_from(get_node_ids(network))


def _add_links(graph, network, weight, default):
    for l in get_links(network):
        e = (l.startnode.id,
             l.endnode.id)
        if isinstance(weight, str):
            weight_value = getattr(l, weight, default)
        elif isinstance(weight, pd.Series) and l.id in weight.index:
            weight_value = weight[l.id]
        else:
            weight_value = default
        graph.add_edge(*e, weight=weight_value, id=l.id)


class Graph:
    """Generates an undirected NetworkX graph from an OOPNET network.

        Note:
            NetworkX Graphs don't support parallel edges between two Nodes. Only one of the parallel edges will be
            present in the Graph object. To allow for parallel pipes, use :class:`oopnet.graph.MultiGraph` instead.

        Args:
          network: OOPNET network object
          weight: name of pipe property as a string which is used as weight (Default value = 'length') or a pandas Series with link IDs as index and weights as values.
          default: When set, the default value is returned as weight for objects that don't have the defined weight attribute or that are missing in the weight pandas Series. Without it, an exception is raised for those objects. (Default value = 0.00001)

        Returns:
            NetworkX Graph object containing all nodes and links in the passed Network.

        Examples:
            The following will create a Graph with link lengths as edge weights (filename needs to be a valid EPANET
            input file):
            >>> network = Network(filename)
            >>> g = Graph(network, 'length')
            Using a simulation result as link weight:
            >>> rpt = Run(network)
            >>> flow = Flow(rpt)
            >>> g = Graph(network, flow)

        """
    def __new__(cls, network: Network, weight: Union[str, pd.Series] = 'length', default: float = 0.00001) -> nx.Graph:
        graph = nx.Graph()
        _add_nodes(graph, network)
        _add_links(graph, network, weight, default)
        return graph


class DiGraph:
    """Generates a directed NetworkX graph from an OOPNET network.

        Args:
          network: OOPNET network object
          weight: name of pipe property as a string which is used as weight (Default value = 'length') or a pandas Series with link IDs as index and weights as values.
          default: When set, the default value is returned as weight for objects that don't have the defined weight attribute or that are missing in the weight pandas Series. Without it, an exception is raised for those objects. (Default value = 0.00001)

        Returns:
            NetworkX DiGraph object containing all nodes and links in the passed Network.

        Examples:
            The following will create a DiGraph with link lengths as edge weights (filename needs to be a valid EPANET
            input file):
            >>> network = Network(filename)
            >>> g = DiGraph(network, 'length')
            Using a simulation result as link weight:
            >>> rpt = Run(network)
            >>> flow = Flow(rpt)
            >>> g = DiGraph(network, flow)

        """
    def __new__(cls, network: Network, weight: Union[str, pd.Series] = 'length', default: float = 0.00001) -> nx.DiGraph:

        g = nx.DiGraph()
        _add_nodes(g, network)
        _add_links(g, network, weight, default)
        return g


class MultiGraph:
    """This function generates an undirected NetworkX graph from an OOPNET network

        Args:
          network: OOPNET network object
          weight: name of pipe property as a string which is used as weight (Default value = 'length') or a pandas Series with link IDs as index and weights as values.
          default: When set, the default value is returned as weight for objects that don't have the defined weight attribute or that are missing in the weight pandas Series. Without it, an exception is raised for those objects. (Default value = 0.00001)

        Returns:
            NetworkX MultiGraph object containing all nodes and links in the passed Network.

        Examples:
            The following will create a MultiGraph with link lengths as edge weights (filename needs to be a valid EPANET
            input file):
            >>> network = Network(filename)
            >>> g = MultiGraph(network, 'length')
            Using a simulation result as link weight:
            >>> rpt = Run(network)
            >>> flow = Flow(rpt)
            >>> g = MultiGraph(network, flow)

        """
    def __new__(cls, network: Network, weight: Union[str, pd.Series] = 'length', default: float = 0.00001) -> nx.MultiGraph:
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


if __name__ == '__main__':
    import os
    from oopnet import *
    filename = os.path.join('..', '..', 'testing', 'networks', 'Poulakis_enhanced_PDA.inp')
    network = Read(filename)
    g = Graph(network)
    # nx.draw(g, nx.get_node_attributes(g, 'coordinates'))
    print()
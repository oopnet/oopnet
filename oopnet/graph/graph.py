from __future__ import annotations
from typing import TYPE_CHECKING, Union
import logging

import networkx as nx
import pandas as pd

from oopnet.utils.getters import get_node_ids, get_links, get_pipes
if TYPE_CHECKING:
    from oopnet.elements import Network

logger = logging.getLogger(__name__)


# todo: add documentation
def _add_nodes(graph, network):
    logger.debug('Adding Node objects to Network')
    graph.add_nodes_from(get_node_ids(network))


def _add_links(graph, network, weight, default):
    logger.debug('Adding Link objects to Network')
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
          weight: name of pipe property as a string which is used as weight or a pandas Series with link IDs as index and weights as values.
          default: When set, the default value is returned as weight for objects that don't have the defined weight attribute or that are missing in the weight pandas Series. Without it, an exception is raised for those objects.

        Returns:
            NetworkX Graph object containing all nodes and links in the passed Network.

        Examples:
            The following will create a Graph with link lengths as edge weights (filename needs to be a valid EPANET input file):
            >>> network = Network(filename)
            >>> g = Graph(network, 'length')
            Using a simulation result as link weight:
            >>> rpt = Run(network)
            >>> flow = Flow(rpt)
            >>> g = Graph(network, flow)

        """
    def __new__(cls, network: Network, weight: Union[str, pd.Series] = 'length', default: float = 0.00001):
        logger.info('Creating Graph object from Network')
        graph = nx.Graph()
        _add_nodes(graph, network)
        _add_links(graph, network, weight, default)
        return graph


class DiGraph:
    """Generates a directed NetworkX graph from an OOPNET network.

        Args:
          network: OOPNET network object
          weight: name of pipe property as a string which is used as weight or a pandas Series with link IDs as index and weights as values.
          default: When set, the default value is returned as weight for objects that don't have the defined weight attribute or that are missing in the weight pandas Series. Without it, an exception is raised for those objects.

        Returns:
            NetworkX DiGraph object containing all nodes and links in the passed Network.

        Examples:
            The following will create a DiGraph with link lengths as edge weights (filename needs to be a valid EPANET input file):
            >>> network = Network(filename)
            >>> g = DiGraph(network, 'length')
            Using a simulation result as link weight:
            >>> rpt = Run(network)
            >>> flow = Flow(rpt)
            >>> g = DiGraph(network, flow)

        """
    def __new__(cls, network: Network, weight: Union[str, pd.Series] = 'length', default: float = 0.00001) -> nx.DiGraph:
        logger.info('Creating DiGraph object from Network')
        graph = nx.DiGraph()
        _add_nodes(graph, network)
        _add_links(graph, network, weight, default)
        return graph


class MultiGraph:
    """Generates an undirected NetworkX graph from an OOPNET network

        Args:
          network: OOPNET network object
          weight: name of pipe property as a string which is used as weight or a pandas Series with link IDs as index and weights as values.
          default: When set, the default value is returned as weight for objects that don't have the defined weight attribute or that are missing in the weight pandas Series. Without it, an exception is raised for those objects.

        Returns:
            NetworkX MultiGraph object containing all nodes and links in the passed Network.

        Examples:
            The following will create a MultiGraph with link lengths as edge weights (filename needs to be a valid EPANET input file):
            >>> network = Network(filename)
            >>> g = MultiGraph(network, 'length')
            Using a simulation result as link weight:
            >>> rpt = Run(network)
            >>> flow = Flow(rpt)
            >>> g = MultiGraph(network, flow)

        """
    def __new__(cls, network: Network, weight: Union[str, pd.Series] = 'length', default: float = 0.00001) -> nx.MultiGraph:
        logger.info('Creating MultiGraph object from Network')
        graph = nx.MultiGraph()
        _add_nodes(graph, network)
        _add_links(graph, network, weight, default)
        return graph


# todo: add documentation
def onlinks2nxlinks(network: Network) -> list[tuple[str, str]]:
    """Converts OOPNET links to NetworkX graph edges.

    Args:
      network: OOPNET network object

    Returns:
        List of tuples in the format (link.startnode.id, link.endnode.id)
    """
    return [(l.startnode.id, l.endnode.id) for l in get_pipes(network)]


def nxlinks2onlinks(G: nx.Graph) -> list[str]:
    """Converts NetworkX graph edges to OOPNET link IDs.

    Args:
      G: NetworkX graph

    Returns:
        List of OOPNET Link IDs
    """
    return [G.get_edge_data(n1, n2)['id'] for n1, n2 in G.edges()]


def edge2pipeid(G: nx.Graph, edge: tuple[str, str]) -> Union[str, list[str]]:
    """Converts an NetworkX edge in a graph to an OOPNET Link ID.

    Args:
      G: NetworkX graph
      edge: NetworkX edge

    Returns:
        ID of corresponding OOPNET Link
    """
    if not isinstance(G, nx.MultiGraph):
        return G.get_edge_data(*edge)['id']
    edges = G.get_edge_data(*edge)
    result = [edges[x]['id'] for x in edges]
    return result if len(result) > 1 else result[0]


def edgeresult2pandas(G: nx.Graph, result: dict) -> pd.Series:
    """Transforms edge data retrieved e.g. from edge centric centrality measurements to a Pandas Series compatible with OOPNET.

    Args:
      G: networkx graph object
      result: dictionary with link IDs as keys

    Returns:
      transformed result into a pandas Series
    """
    return_dict = {}
    for edge in list(result.keys()):
        pipe = edge2pipeid(G, edge)
        if isinstance(pipe, list):
            for lid in pipe:
                return_dict[lid] = result[edge]
        else:
            return_dict[pipe] = result[edge]
    return pd.Series(return_dict)


if __name__ == '__main__':
    import os
    from oopnet import *
    filename = os.path.join('..', '..', 'testing', 'networks', 'Poulakis_enhanced_PDA.inp')
    network = Read(filename)
    g = Graph(network)
    # nx.draw(g, nx.get_node_attributes(g, 'coordinates'))
    print()
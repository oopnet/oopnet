from __future__ import annotations

from typing import TYPE_CHECKING, Union

from oopnet.utils.getters.element_lists import get_links, get_inflow_nodes

if TYPE_CHECKING:
    from oopnet.elements.network import Network
    from oopnet.elements.network_components import Link, Node


def _filter_sort(alist: list[Union[Node, Link]]) -> list[Union[Node, Link]]:
    """Filters and sorts Nodes and Links in a list.

    Filters duplicates and sorts NetworkComponent by ID.

    Args:
        alist: list of either Nodes or Links

    Returns:
        list of sorted and filtered Node or List objects

    """
    alist.sort(key=lambda x: x.id)
    if len({x.id for x in alist}) == len(alist):
        return alist
    adict = {x.id: x for x in alist}
    return list(adict.values())


def get_neighbor_links(network: Network, query_link: Link) -> list[Link]:
    """Gets Links that share a Node with the passed Link.

    Args:
        network: Network in which the query is executed
        query_link: Link that the query is based on

    Returns:
        list of Links that are connected to the passed Link

    """
    nodes = [query_link.startnode, query_link.endnode]
    return [link for link in get_links(network) if any(node in nodes for node in [link.startnode, link.endnode]) and
            link != query_link]


def get_next_neighbor_links(network: Network, query_link: Link) -> list[Link]:
    """Gets Links that share a Node with the neighbors of the passed Link.

    Args:
        network: Network in which the query is executed
        query_link: Link that the query is based on

    Returns:
        list of Links that are connected to the passed Link

    """
    neigh_links = get_neighbor_links(network, query_link)
    nextneigh_links = [x for link in neigh_links for x in get_neighbor_links(network, link) if x != query_link and x not in neigh_links]
    return _filter_sort(nextneigh_links)


def get_adjacent_links(network: Network, query_node: Node) -> list[Link]:
    """Gets Links that are connected to query_node.

    Args:
        network: Network in which the query is executed
        query_node: Node that the query is based on

    Returns:
        list of Links that are connected to the passed Node

    """
    adj_links = [x for x in get_links(network) if query_node in [x.startnode, x.endnode]]
    return _filter_sort(adj_links)


def get_neighbor_nodes(network: Network, query_node: Node) -> list[Node]:
    """Gets Nodes that are connected to query_node with any sort of Link.

    Args:
        network: Network in which the query is executed
        query_node: Node that the query is based on

    Returns:
        list of Nodes that are connected to the passed Node

    """
    adj_links = get_adjacent_links(network, query_node)
    neigh_nodes = [x.startnode if x.startnode != query_node else x.endnode for x in adj_links]
    return _filter_sort(neigh_nodes)


def get_next_neighbor_nodes(network: Network, query_node: Node) -> list[Node]:
    """Gets Nodes that are connected to neighbor Nodes of query_node with any sort of Link.

    Args:
        network: Network in which the query is executed
        query_node: Node that the query is based on

    Returns:
        list of Nodes that are connected to the passed Node's neighbors

    """
    neigh_nodes = get_neighbor_nodes(network, query_node)
    nextneigh_nodes = [x for node in neigh_nodes for x in get_neighbor_nodes(network, node) if x != query_node and x not in neigh_nodes]
    return _filter_sort(nextneigh_nodes)


def get_inflow_neighbor_nodes(network: Network) -> list[Node]:
    """Gets Nodes that are connected to the inflow Nodes with any sort of Link.

    Args:
        network: Network in which the query is executed

    Return:
        list of Nodes that are connected with Network's inflow Nodes

    """
    neigh_nodes = []
    for inflow in get_inflow_nodes(network):
        neigh_nodes.extend(get_neighbor_nodes(network, inflow))
    return _filter_sort(neigh_nodes)

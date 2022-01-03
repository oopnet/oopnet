import pandas as pd

from oopnet.utils.getters.element_lists import get_links, get_link_ids, get_pipes, get_pipe_ids, get_nodes, \
    get_node_ids, get_junction_ids, get_junctions, get_valve_ids, get_valves, get_pumps, get_pump_ids
from oopnet.elements.network import Network
"""
Functions for getting network properties as pandas dataframes
"""


# Links:
def get_startnodes(network: Network) -> pd.Series:
    """Get all startnodes of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      startnodes as pandas.Series

    """
    values = [x.startnode for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'startnodes'
    return series


def get_endnodes(network: Network) -> pd.Series:
    """Get all endnodes of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      endnodes as pandas.Series

    """
    values = [x.endnode for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'endnodes'
    return series


def get_startendnodes(network: Network) -> pd.Series:
    """Get all endnodes of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      endnodes as pandas.Series

    """
    s1 = get_startnodes(network)
    s2 = get_endnodes(network)
    return pd.concat([s1, s2], axis=1)


def get_startendcoordinates(network: Network) -> pd.DataFrame:
    """Get all start and end coordinates of all links in the network as a pandas dataframe

    Args:
      network: OOPNET network object

    Returns:
      start/end x-y-coordinates as pd.Dataframe

    """
    se = get_startendnodes(network)
    ids = se.index
    sx = [x.xcoordinate for x in se['startnodes']]
    sy = [x.ycoordinate for x in se['startnodes']]
    ex = [x.xcoordinate for x in se['endnodes']]
    ey = [x.ycoordinate for x in se['endnodes']]
    return pd.DataFrame(index=ids, data={'start x-coordinate': sx,
                                         'start y-coordinate': sy,
                                         'end x-coordinate': ex,
                                         'end y-coordinate': ey})


def get_initialstatus(network: Network) -> pd.Series:
    """Get all initial status of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      initial status as pandas.Series

    """
    values = [x.initialstatus for x in get_pumps(network) + get_valves(network)]
    names = get_pump_ids(network) + get_valve_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'intial status'
    return series


def get_status(network: Network) -> pd.Series:
    """Get all status of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      status as pandas.Series

    """
    values = [x.status for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'status'
    return series


def get_setting(network: Network) -> pd.Series:
    """Get all settings of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      settings as pandas.Series

    """
    values = [x.setting for x in get_pumps(network) + get_valves(network)]
    names = get_pump_ids(network) + get_valve_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'setting'
    return series


def get_linkcenter_coordinates(network: Network) -> pd.DataFrame:
    """Get the center coordinates of all links in the network as a pandas Dataframe

    Args:
      network: OOPNET network object

    Returns:
      coordinates as pandas.Dataframe

    """
    x = [(x.startnode.xcoordinate + x.endnode.xcoordinate) / 2 for x in get_links(network)]
    y = [(x.startnode.ycoordinate + x.endnode.ycoordinate) / 2 for x in get_links(network)]
    return pd.DataFrame(index=get_link_ids(network), data={'center x-coordinate': x, 'center y-coordinate': y})


def get_link_comment(network: Network) -> pd.Series:
    """Get all comments of all links in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      comments as pandas.Series

    """
    values = [x.comment for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'link comment'
    return series


# Pipes
def get_length(network: Network) -> pd.Series:
    """Get all length values of all pipes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      length as pandas.Series

    """
    values = [x.length for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe lengths'
    series.units = 'm'
    return series


def get_diameter(network: Network) -> pd.Series:
    """Get all diameter values of all pipes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      diameter as pandas.Series

    """
    ids = []
    diameters = []
    if network.pipes:
        ids.extend(get_pipe_ids(network))
        diameters.extend([x.diameter for x in get_pipes(network)])
    if network.valves:
        ids.extend(get_valve_ids(network))
        diameters.extend([x.diameter for x in get_valves(network)])
    series = pd.Series(data=diameters, index=ids)
    series.name = 'pipe diameters'
    series.units = 'mm'
    return series


def get_roughness(network: Network) -> pd.Series:
    """Get all roughness values of all pipes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      roughness as pandas.Series

    """
    values = [x.roughness for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe roughness'
    series.units = 'mm' if network.options.headloss == 'D-W' else '1'
    return series


def get_minorloss(network: Network) -> pd.Series:
    """Get all minor-loss values of all pipes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      minor-loss as pandas.Series

    """
    values = [x.minorloss for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe minor-losses'
    series.units = '1'
    return series


# ToDo: Add quality parameters for links

# Nodes:
def get_xcoordinate(network: Network) -> pd.Series:
    """Get all xcoordinate values of all nodes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      xcoordinate as pandas.Series

    """
    values = [x.xcoordinate for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node x-coordinate'
    series.units = '1'
    return series


def get_ycoordinate(network: Network) -> pd.Series:
    """Get all ycoordinate values of all nodes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      ycoordinate as pandas.Series

    """
    values = [x.ycoordinate for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node y-coordinate'
    series.units = '1'
    return series


def get_coordinates(network: Network) -> pd.DataFrame:
    """Get all x and y coordinate values of all nodes in the network as a pandas Dataframe

    Args:
      network: OOPNET network object

    Returns:
      x-y-coordinate as pandas.Dataframe

    """
    s1 = get_xcoordinate(network)
    s2 = get_ycoordinate(network)
    series = pd.concat([s1, s2], axis=1)
    return series


def get_elevation(network: Network) -> pd.Series:
    """Get all elevation values of all nodes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      elevations as pandas.Series

    """
    values = [x.elevation for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node elevation'
    series.units = 'm'
    return series


def get_basedemand(network: Network) -> pd.Series:
    """Get all base demand values of all junctions in the netwokr as a pandas series (Build the sum if more than one base
    demand exists for a single junction)

    Args:
      network: OOPNET network object

    Returns:
      base demands as pandas.Series

    """
    values = [sum(x.demand) if isinstance(x.demand, list) else x.demand for x in get_junctions(network)]
    names = get_junction_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'base demand'
    series.units = 'L/s'
    return series


def get_node_comment(network: Network) -> pd.Series:
    """Get all comments of all nodes in the network as a pandas series

    Args:
      network: OOPNET network object

    Returns:
      comments as pandas.Series

    """
    values = [x.comment for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node comment'
    return series

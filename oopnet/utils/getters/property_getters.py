from __future__ import annotations
from typing import TYPE_CHECKING

import pandas as pd

from oopnet.utils.getters.element_lists import get_links, get_link_ids, get_pipes, get_pipe_ids, get_nodes, \
    get_node_ids, get_junction_ids, get_junctions, get_valve_ids, get_valves, get_pumps, get_pump_ids

if TYPE_CHECKING:
    from oopnet.elements.network import Network


# Links:
def get_startnodes(network: Network) -> pd.Series:
    """Gets all start nodes of all Links in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Link IDs as index and start nodes as values.

    """
    values = [x.startnode for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'startnodes'
    return series


def get_endnodes(network: Network) -> pd.Series:
    """Gets all end nodes of all Links in the Network as a pandas Series..

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Link IDs as index and end nodes as values.

    """
    values = [x.endnode for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'endnodes'
    return series


def get_startendnodes(network: Network) -> pd.DataFrame:
    """Gets all endnodes of all Links in the Network as a pandas DataFrame.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas DataFrame with Link IDs as index and a column for start and end nodes respectively.

    """
    s1 = get_startnodes(network)
    s2 = get_endnodes(network)
    return pd.concat([s1, s2], axis=1)


def get_startendcoordinates(network: Network) -> pd.DataFrame:
    """Gets all start and end coordinates of all Links in the Network as a pandas DataFrame.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas DataFrame with Link IDs as index and a column for start and end node x and y coordinates respectively.

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


# def get_initialstatus(network: Network) -> pd.Series:
#     """Gets all initial status of all Links in the Network as a pandas Series.
#
#     Args:
#       network: OOPNET Network object
#
#     Returns:
#       Pandas Series with Link IDs as index and initial status as values.
#
#     """
#     values = [x.initialstatus for x in get_pumps(network) + get_valves(network)]
#     names = get_pump_ids(network) + get_valve_ids(network)
#     series = pd.Series(data=values, index=names)
#     series.name = 'intial status'
#     return series


def get_status(network: Network) -> pd.Series:
    """Gets all status of all Links in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Link IDs as index and status as values.

    """
    values = [x.status for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'status'
    return series


def get_setting(network: Network) -> pd.Series:
    """Gets all settings of all Pumps and Valves in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Pump/Valve IDs as index and settings as values.

    """
    values = [x.setting for x in get_pumps(network) + get_valves(network)]
    names = get_pump_ids(network) + get_valve_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'setting'
    return series


def get_linkcenter_coordinates(network: Network) -> pd.DataFrame:
    """Get the center coordinates of all Links in the Network as a pandas Dataframe.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas DataFrame with Link IDs as index and the Links' center x and y coordinates as columns.

    """
    x = [(x.startnode.xcoordinate + x.endnode.xcoordinate) / 2 for x in get_links(network)]
    y = [(x.startnode.ycoordinate + x.endnode.ycoordinate) / 2 for x in get_links(network)]
    return pd.DataFrame(index=get_link_ids(network), data={'center x-coordinate': x, 'center y-coordinate': y})


def get_link_comment(network: Network) -> pd.Series:
    """Gets all comments of all Links in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Link IDs as index and comments as values.

    """
    values = [x.comment for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'link comment'
    return series


# Pipes
def get_length(network: Network) -> pd.Series:
    """Gets all length values of all Pipes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Pink IDs as index and lengths as values.

    """
    values = [x.length for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe lengths'
    series.units = 'm'
    return series


def get_diameter(network: Network) -> pd.Series:
    """Gets all diameter values of all Pipes and Valves in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Pipe/Valve IDs as index and diameters as values.

    """
    ids = []
    diameters = []
    ids.extend(get_pipe_ids(network))
    diameters.extend([x.diameter for x in get_pipes(network)])
    ids.extend(get_valve_ids(network))
    diameters.extend([x.diameter for x in get_valves(network)])
    series = pd.Series(data=diameters, index=ids)
    series.name = 'pipe diameters'
    series.units = 'mm'
    return series


def get_roughness(network: Network) -> pd.Series:
    """Gets all roughness values of all Pipes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Pipe IDs as index and roughness values as values.

    """
    values = [x.roughness for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe roughness'
    series.units = 'mm' if network.options.headloss == 'D-W' else '1'
    return series


def get_minorloss(network: Network) -> pd.Series:
    """Gets all minor loss coefficient values of all Pipes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Pipe IDs as index and minor loss coefficients as values.

    """
    values = [x.minorloss for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe minor-losses'
    series.units = '1'
    return series


# ToDo: Add quality parameters for Links

# Nodes:
def get_xcoordinate(network: Network) -> pd.Series:
    """Gets all x coordinate values of all Nodes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Node IDs as index and x coordinates as values.

    """
    values = [x.xcoordinate for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node x-coordinate'
    series.units = '1'
    return series


def get_ycoordinate(network: Network) -> pd.Series:
    """Gets all y coordinate values of all Nodes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Node IDs as index and y coordinates as values.

    """
    values = [x.ycoordinate for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node y-coordinate'
    series.units = '1'
    return series


def get_coordinates(network: Network) -> pd.DataFrame:
    """Gets all x and y coordinate values of all Nodes in the Network as a pandas Dataframe

    Args:
      network: OOPNET Network object

    Returns:
      Pandas DataFrame with Node IDs as index and x and y coordinates as columns.

    """
    s1 = get_xcoordinate(network)
    s2 = get_ycoordinate(network)
    return pd.concat([s1, s2], axis=1)


def get_elevation(network: Network) -> pd.Series:
    """Gets all elevation values of all Nodes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Node IDs as index and elevations as values.

    """
    values = [x.elevation for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node elevation'
    series.units = 'm'
    return series


def get_basedemand(network: Network) -> pd.Series:
    """Gets all base demand values of all Junctions in the Network as a pandas Series.
    
    Builds the sum if more than one base demand exists for a single junction.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Node IDs as index and base demands as values.

    """
    values = [sum(x.demand) if isinstance(x.demand, list) else x.demand for x in get_junctions(network)]
    names = get_junction_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'base demand'
    series.units = 'L/s'
    return series


def get_node_comment(network: Network) -> pd.Series:
    """Gets all comments of all Nodes in the Network as a pandas Series.

    Args:
      network: OOPNET Network object

    Returns:
      Pandas Series with Node IDs as index and comments as values.

    """
    values = [x.comment for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node comment'
    return series

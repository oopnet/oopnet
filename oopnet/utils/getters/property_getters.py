import pandas as pd
from oopnet.utils.getters.element_lists import get_links, get_link_ids, get_pipes, get_pipe_ids, get_nodes, \
    get_node_ids, get_junction_ids, get_junctions

"""
Functions for getting network properties as pandas dataframes
"""

# Links:
def get_startnodes(network):
    """
    Get all startnodes of all links in the network as a pandas series
    :param network: OOPNET network object
    :return: startnodes as pandas.Series
    """
    values = [x.startnode for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'startnodes'
    return series


def get_endnodes(network):
    """
    Get all endnodes of all links in the network as a pandas series
    :param network: OOPNET network object
    :return: endnodes as pandas.Series
    """
    values = [x.endnode for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'endnodes'
    return series


def get_startendnodes(network):
    """
    Get all endnodes of all links in the network as a pandas series
    :param network: OOPNET network object
    :return: endnodes as pandas.Series
    """
    s1 = get_startnodes(network)
    s2 = get_endnodes(network)
    series = pd.concat([s1, s2], axis=1)
    return series


def get_startendcoordinates(network):
    """
    Get all start and end coordinates of all links in the network as a pandas dataframe
    :param network: OOPNET network object
    :return: start/end x-y-coordinates as pd.Dataframe
    """
    se = get_startendnodes(network)
    ids = se.index
    sx = [x.xcoordinate for x in se['startnodes']]
    sy = [x.ycoordinate for x in se['startnodes']]
    ex = [x.xcoordinate for x in se['endnodes']]
    ey = [x.ycoordinate for x in se['endnodes']]
    df = pd.DataFrame(index=ids, data={'start x-coordinate': sx,
                                       'start y-coordinate': sy,
                                       'end x-coordinate': ex,
                                       'end y-coordinate': ey})
    return df


def get_intialstatus(network):
    """
    Get all initial status of all links in the network as a pandas series
    :param network: OOPNET network object
    :return: initial status as pandas.Series
    """
    values = [x.intialstatus for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'intial status'
    return series


def get_status(network):
    """
    Get all status of all links in the network as a pandas series
    :param network: OOPNET network object
    :return: status as pandas.Series
    """
    values = [x.status for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'status'
    return series


def get_setting(network):
    """
    Get all settings of all links in the network as a pandas series
    :param network: OOPNET network object
    :return: settings as pandas.Series
    """
    values = [x.setting for x in get_links(network)]
    names = get_link_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'setting'
    return series


# Pipes
def get_length(network):
    """
    Get all length values of all pipes in the network as a pandas series
    :param network: OOPNET network object
    :return: length as pandas.Series
    """
    values = [x.length for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe lengths'
    series.units = 'm'
    return series


def get_diameter(network):
    """
    Get all diameter values of all pipes in the network as a pandas series
    :param network: OOPNET network object
    :return: diameter as pandas.Series
    """
    values = [x.diameter for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe diameters'
    series.units = 'mm'
    return series

def get_roughness(network):
    """
    Get all roughness values of all pipes in the network as a pandas series
    :param network: OOPNET network object
    :return: roughness as pandas.Series
    """
    values = [x.roughness for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe roughness'
    if network.options.headloss == 'D-W':
        series.units = 'mm'
    else:
        series.units = '1'
    return series


def get_minorloss(network):
    """
    Get all minor-loss values of all pipes in the network as a pandas series
    :param network: OOPNET network object
    :return: minor-loss as pandas.Series
    """
    values = [x.minorloss for x in get_pipes(network)]
    names = get_pipe_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'pipe minor-losses'
    series.units = '1'
    return series


# ToDo: Add quality parameters for links

# Nodes:
def get_xcoordinate(network):
    """
    Get all xcoordinate values of all nodes in the network as a pandas series
    :param network: OOPNET network object
    :return: xcoordinate as pandas.Series
    """
    values = [x.xcoordinate for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node x-coordinate'
    series.units = '1'
    return series


def get_ycoordinate(network):
    """
    Get all ycoordinate values of all nodes in the network as a pandas series
    :param network: OOPNET network object
    :return: ycoordinate as pandas.Series
    """
    values = [x.ycoordinate for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node y-coordinate'
    series.units = '1'
    return series

def get_coordinates(network):
    """
    Get all x and y coordinate values of all nodes in the network as a pandas series
    :param network: OOPNET network object
    :return: x-y-coordinate as pandas.Dataframe
    """
    s1 = get_xcoordinate(network)
    s2 = get_ycoordinate(network)
    series = pd.concat([s1, s2], axis=1)
    return series


def get_elevation(network):
    """
    Get all elevation values of all nodes in the network as a pandas series
    :param network: OOPNET network object
    :return: elevations as pandas.Series
    """
    values = [x.elevation for x in get_nodes(network)]
    names = get_node_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'node elevation'
    series.units = 'm'
    return series


def get_basedemand(network):
    """
    Get all base demand values of all junctions in the netwokr as a pandas series (Build the sum if more than one base
    demand exists for a single junction)
    :param network: OOPNET network object
    :return: base demands as pandas.Series
    """
    values = [sum(x.demand) if isinstance(x.demand, list) else x.demand for x in get_junctions(network)]
    names = get_junction_ids(network)
    series = pd.Series(data=values, index=names)
    series.name = 'base demand'
    series.units = 'L/s'
    return series


# if __name__ == '__main__':
#
#     net = Read(os.path.join('..', '..', '..', 'examples', 'data', 'C-town.inp'))
#     df = get_coordinates(net)
#     df = df - df.mean()
#
#     df =  -np.abs(df.sum(axis=1))
#     # df = (df - df.mean()).sum(axis=1)
#     # print df
#     Plot(net, nodes=df, colormap='viridis')
#     Show()
#

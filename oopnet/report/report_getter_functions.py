__author__ = 'davidsteffelbauer'
from oopnet.utils.getters.property_getters import get_length

def elevation(report):
    """
    Function for getting the elevations from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the elevations of the nodes
    """
    nodes, links = report
    df = nodes.sel(vars='Elevation').to_pandas()
    df.name = 'Elevation (m)'
    return df


def demand(report):
    """
    Function for getting the demands from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the demands of the nodes
    """
    nodes, links = report
    df = nodes.sel(vars='Demand').to_pandas()
    df.name = 'Demand (l/s)'
    return df


def head(report):
    """
    Function for getting the heads from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the heads of the nodes
    """
    nodes, links = report
    df = nodes.sel(vars='Head').to_pandas()
    df.name = 'Head (m)'
    return df


def pressure(report):
    """
    Function for getting the pressures from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the pressures of the nodes
    """
    nodes, links = report
    df = nodes.sel(vars='Pressure').to_pandas()
    df.name = 'Pressure (m)'
    return df


def quality(report):
    """
    Function for getting the qualities from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the qualities of the nodes
    """
    nodes, links = report
    df = nodes.sel(vars='Quality').to_pandas()
    df.name = 'Quality'  # Todo: Add units to Quality
    return df


def length(report):
    """
    Function for getting the lengths from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the lengths of the links
    """
    nodes, links = report
    df = links.sel(vars='Length').to_pandas()
    df.name = 'Length (m)'
    return df


def diameter(report):
    """
    Function for getting the diameters from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the diameters of the links
    """
    nodes, links = report
    df = links.sel(vars='Diameter').to_pandas()
    df.name = 'Diameter (m)'
    return df


def flow(report):
    """
    Function for getting the flows from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the flows of the links
    """
    nodes, links = report
    df = links.sel(vars='Flow').to_pandas()
    df.name = 'Flow (l/s)'
    return df


def velocity(report):
    """
    Function for getting the velocities from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the velocities of the links
    """
    nodes, links = report
    df = links.sel(vars='Velocity').to_pandas()
    df.name = 'Velocity (m/s)'
    return df


def headlossper1000m(report):
    """
    Function for getting the headlosses from a simulation report object as it is in the report (units in headloss per 1000m)

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the headlosses of the links
    """
    nodes, links = report
    df = links.sel(vars='Headloss').to_pandas()
    df.name = 'Headloss (/1000m)'
    return df


def headloss(report):
    """
    Function for getting the headlosses from a simulation report object

    WARNING: If one wants to work with headloss, then the length has to be defined in the report

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the headlosses of the links
    """
    nodes, links = report
    df = links.sel(vars='Headloss').to_pandas()
    df = (df*length(report)/1000.0)
    df.name = 'Headloss (m)'
    return df


def position(report):
    """
    Function for getting the positions from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the positions of the links
    """
    nodes, links = report
    df = links.sel(vars='Position').to_pandas()
    df.name = 'Position'
    return df


def setting(report):
    """
    Function for getting the settings from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the settings of the links
    """
    nodes, links = report
    df = links.sel(vars='Setting').to_pandas()
    df.name = 'Setting'
    return df


def reaction(report):
    """
    Function for getting the reactions from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the reactions of the links
    """
    nodes, links = report
    df = links.sel(vars='Reaction').to_pandas()
    df.name = 'Reaction (mass/L/day)'
    return df


def ffactor(report):
    """
    Function for getting the ffactors from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the ffactors of the links
    """
    nodes, links = report
    df = links.sel(vars='F-Factor').to_pandas()
    df.name = 'Friction Factor'
    return df


def nodeinfo(report, nodename):
    """
    Function for getting the node informations from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the informations of the nodes
    """
    nodes, links = report
    df = nodes.sel(id=nodename).to_pandas()
    df.name = nodename
    return df


def linkinfo(report, linkname):
    """
    Function for getting the link informations from a simulation report object

    :param report: OOPNET simulation report
    :return: Pandas Dataframe containing the informations of the links
    """
    nodes, links = report
    df = links.sel(id=linkname).to_pandas()
    df.name = linkname
    return df

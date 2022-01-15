import pandas as pd

from oopnet.report.xrayreport import Report


def elevation(report: Report) -> pd.Series:
    """Function for getting the elevations from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the elevations of the nodes

    """
    nodes, links = report
    data = nodes.sel(vars='Elevation').to_pandas()
    data.name = 'Elevation (m)'
    return data


def demand(report: Report) -> pd.Series:
    """Function for getting the demands from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the demands of the nodes

    """
    nodes, links = report
    data = nodes.sel(vars='Demand').to_pandas()
    data.name = 'Demand (l/s)'
    return data


def head(report: Report) -> pd.Series:
    """Function for getting the heads from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the heads of the nodes

    """
    nodes, links = report
    data = nodes.sel(vars='Head').to_pandas()
    data.name = 'Head (m)'
    return data


def pressure(report: Report) -> pd.Series:
    """Function for getting the pressures from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the pressures of the nodes

    """
    nodes, links = report
    data = nodes.sel(vars='Pressure').to_pandas()
    data.name = 'Pressure (m)'
    return data


def quality(report: Report) -> pd.Series:
    """Function for getting the qualities from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the qualities of the nodes

    """
    nodes, links = report
    data = nodes.sel(vars='Quality').to_pandas()
    data.name = 'Quality'  # Todo: Add units to Quality
    return data


def length(report: Report) -> pd.Series:
    """Function for getting the lengths from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the lengths of the links

    """
    nodes, links = report
    data = links.sel(vars='Length').to_pandas()
    data.name = 'Length (m)'
    return data


def diameter(report: Report) -> pd.Series:
    """Function for getting the diameters from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the diameters of the links

    """
    nodes, links = report
    data = links.sel(vars='Diameter').to_pandas()
    data.name = 'Diameter (m)'
    return data


def flow(report: Report) -> pd.Series:
    """Function for getting the flows from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the flows of the links

    """
    nodes, links = report
    data = links.sel(vars='Flow').to_pandas()
    data.name = 'Flow (l/s)'
    return data


def velocity(report: Report) -> pd.Series:
    """Function for getting the velocities from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the velocities of the links

    """
    nodes, links = report
    data = links.sel(vars='Velocity').to_pandas()
    data.name = 'Velocity (m/s)'
    return data


def headlossper1000m(report: Report) -> pd.Series:
    """Function for getting the headlosses from a simulation report object as it is in the report (units in headloss
    per 1000m)

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the headlosses of the links

    """
    nodes, links = report
    data = links.sel(vars='Headloss').to_pandas()
    data.name = 'Headloss (/1000m)'
    return data


def headloss(report: Report) -> pd.Series:
    """Function for getting the headlosses from a simulation report object.
    
    WARNING: If one wants to work with headloss, then the length has to be defined in the report

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the headlosses of the links

    """
    nodes, links = report
    data = links.sel(vars='Headloss').to_pandas()
    data = (data*length(report)/1000.0)
    data.name = 'Headloss (m)'
    return data


def position(report: Report) -> pd.Series:
    """Function for getting the positions from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the positions of the links

    """
    nodes, links = report
    data = links.sel(vars='Position').to_pandas()
    data.name = 'Position'
    return data


def setting(report: Report) -> pd.Series:
    """Function for getting the settings from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the settings of the links

    """
    nodes, links = report
    data = links.sel(vars='Setting').to_pandas()
    data.name = 'Setting'
    return data


def reaction(report: Report) -> pd.Series:
    """Function for getting the reactions from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the reactions of the links

    """
    nodes, links = report
    data = links.sel(vars='Reaction').to_pandas()
    data.name = 'Reaction (mass/L/day)'
    return data


def ffactor(report: Report) -> pd.Series:
    """Function for getting the ffactors from a simulation report object.

    Args:
      report: OOPNET simulation report

    Returns:
      Pandas Series containing the ffactors of the links

    """
    nodes, links = report
    data = links.sel(vars='F-Factor').to_pandas()
    data.name = 'Friction Factor'
    return data


def nodeinfo(report: Report, nodename: str) -> pd.Series:
    """Function for getting the node informations from a simulation report object.

    Args:
      report: OOPNET simulation report
      nodename: node ID

    Returns:
      Pandas Series containing the information of the nodes

    """
    nodes, links = report
    data = nodes.sel(id=nodename).to_pandas()
    data.name = nodename
    return data


def linkinfo(report: Report, linkname: str) -> pd.Series:
    """Function for getting the link informations from a simulation report object.

    Args:
      report: OOPNET simulation report
      linkname: link ID

    Returns:
      Pandas Series containing the information of the links

    """
    nodes, links = report
    data = links.sel(id=linkname).to_pandas()
    data.name = linkname
    return data

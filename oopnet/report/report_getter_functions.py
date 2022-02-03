import pandas as pd

from oopnet.report.xrayreport import Report


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

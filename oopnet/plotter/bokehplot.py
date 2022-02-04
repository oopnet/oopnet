import numpy as np
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource
import matplotlib.cm as cmx
from matplotlib import pyplot as plt
import matplotlib.colors as colors

from oopnet.utils.getters import get_link_ids, get_node_ids, get_junctions, get_tanks, get_reservoirs, get_pipes, \
    get_pumps, get_valves


# todo: refactor
def convert_to_hex(rgba_color):
    """

    Args:
      rgba_color: 

    Returns:

    """
    red = int(rgba_color[0]*255)
    green = int(rgba_color[1]*255)
    blue = int(rgba_color[2]*255)
    return '#{r:02x}{g:02x}{b:02x}'.format(r=red, g=green, b=blue)


def colorfun(series, colormap='jet'):
    """

    Args:
      series: 
      colormap:  (Default value = 'jet')

    Returns:

    """
    values = series.values
    cm = plt.get_cmap(colormap)
    cNorm = colors.Normalize(vmin=np.nanmin(values), vmax=np.nanmax(values))
    scalar_map = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    scalar_map._A = []
    rgba = list(map(scalar_map.to_rgba, values))
    return list(map(convert_to_hex, rgba))


def outsidelist(element, colorhash):
    """

    Args:
      element: 
      colorhash: 

    Returns:

    """
    if element in colorhash:
        return colorhash[element]
    else:
        return 'k'


def plotnode(f, elements, colors, marker='o'):
    """

    Args:
      f: 
      elements: 
      colors: 
      marker:  (Default value = 'o')

    Returns:

    """
    x = [x.xcoordinate for x in elements]
    y = [x.ycoordinate for x in elements]
    c = [outsidelist(x.id, colors) for x in elements]
    c = [convert_to_hex(x) for x in c]
    if marker == 'o':
        f.circle(x, y, color=c, size=8.0)
    if marker == 's':
        f.square(x, y, color=c, size=8.0)
    if marker == 'D':
        f.square(x, y, color=c, size=8.0, angle=np.pi/4)


def plotlink(f, elements, colors, marker='o'):
    """

    Args:
      f: 
      elements: 
      colors: 
      marker:  (Default value = 'o')

    Returns:

    """

    xs = [x.startnode.xcoordinate for x in elements]
    xe = [x.endnode.xcoordinate for x in elements]
    ys = [x.startnode.ycoordinate for x in elements]
    ye = [x.endnode.ycoordinate for x in elements]

    x = 0.5 * (np.asarray(xs) + np.asarray(xe))
    y = 0.5 * (np.asarray(ys) + np.asarray(ye))

    c = [outsidelist(x.id, colors) for x in elements]
    c = [convert_to_hex(x) for x in c]

    f.segment(x0=xs, x1=xe, y0=ys, y1=ye, color=c, line_width=2.0)

    if marker == 'v':
        f.triangle(x, y, color=c, size=8.0)
    if marker == 'p':
        f.inverted_triangle(x, y, color=c, size=8.0)


class Plotsimulation:
    """This function plots OOPNET networks with simulation results as a network plot with Bokehplot.
    
    Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.
    
    Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars standing on their top in the middle, Pumps are plotted as lines with triangulars standing on an edge

    Args:
      network: OOPNET network object one wants to plot
      tools: tools used for the Bokeh plot (panning, zooming, ...)
      nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
      links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)). f links is None or specific links do not have  values, then the links are drawn as black lines
      colormap: Colormap defining which colors are used for the simulation results (default is matplotlib's colormap jet). colormap can either be a string for matplotlib colormaps, a matplotlib.colors.LinearSegmentedColormap object or a matplotlib.colors.ListedColormap object. If one wants to use different colormaps for nodes and links, then make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colormaps = {'node':'jet', 'link':'cool'} plots nodes with colormap jet and links using colormap cool)

    Returns:
      Bokehplot's figure handle

    """
    def __new__(self, network, tools=None, links=None, nodes=None, colormap='jet'):

        if isinstance(colormap, str):
            n_cmap = plt.get_cmap(colormap)
            l_cmap = plt.get_cmap(colormap)
        elif isinstance(colormap, colors.LinearSegmentedColormap) or \
                isinstance(colormap, colors.ListedColormap):
            n_cmap = colormap
            l_cmap = colormap
        elif isinstance(colormap, dict):
            if 'node' in colormap:
                if isinstance(colormap['node'], str):
                    n_cmap = plt.get_cmap(colormap['node'])
                elif isinstance(colormap['node'], colors.LinearSegmentedColormap) or \
                        isinstance(colormap['node'], colors.ListedColormap):
                    n_cmap = colormap['node']
            else:
                n_cmap = plt.get_cmap('jet')

            if 'link' in colormap:
                if isinstance(colormap['link'], str):
                    l_cmap = plt.get_cmap(colormap['link'])
                elif isinstance(colormap['link'], colors.LinearSegmentedColormap) or \
                        isinstance(colormap['link'], colors.ListedColormap):
                    l_cmap = colormap['link']
            else:
                l_cmap = plt.get_cmap('jet')

        if tools:
            f = figure(tools=tools)
        else:
            f = figure()

        # Links
        if links is None:
            linklist = get_link_ids(network)
            linkcolors = pd.Series(['k'] * len(linklist), index=linklist)

        else:
            cnorm = colors.Normalize(vmin=np.nanmin(links.values), vmax=np.nanmax(links.values))
            scalar_map = cmx.ScalarMappable(norm=cnorm, cmap=l_cmap)
            scalar_map._A = []
            linkcolors = links.apply(scalar_map.to_rgba)

        plotlink(f, get_pipes(network), linkcolors, marker=None)

        plotlink(f, get_valves(network), linkcolors, marker='v')

        plotlink(f, get_pumps(network), linkcolors, marker='p')

        # Nodes
        if nodes is None:
            nodelist = get_node_ids(network)
            nodecolors = pd.Series(['k'] * len(nodelist), index=nodelist)
        else:
            cnorm = colors.Normalize(vmin=np.nanmin(nodes.values), vmax=np.nanmax(nodes.values))
            scalar_map = cmx.ScalarMappable(norm=cnorm, cmap=n_cmap)
            scalar_map._A = []
            nodecolors = nodes.apply(scalar_map.to_rgba)

        plotnode(f, get_junctions(network), nodecolors, marker='o')

        plotnode(f, get_tanks(network), nodecolors, marker='s')

        plotnode(f, get_reservoirs(network), nodecolors, marker='D')

        f.axis.visible = False
        return f

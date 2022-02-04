from __future__ import annotations
from typing import Union, Optional, Type, TYPE_CHECKING

import matplotlib.axes
from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.collections import LineCollection
import networkx as nx
import numpy as np
import pandas as pd

from oopnet.elements.network_components import Junction, Reservoir, Tank, Pipe, Pump, Valve
from oopnet.utils.getters.element_lists import get_link_ids, get_node_ids, get_valves, get_pumps, get_junctions, \
    get_reservoirs, get_tanks, get_pipes
if TYPE_CHECKING:
    from oopnet.elements.network import Network


# todo: refactor
class Plotnodes:
    """ """

    def __new__(cls, nodes: list, nodetype: Union[Type[Junction], Type[Reservoir], Type[Tank]], color: pd.Series,
                ms: float, zorder: int, nodetruncate: bool = False):
        nid = []
        x = []
        y = []

        for node in nodes:
            nid.append(node.id)
            x.append(node.xcoordinate)
            y.append(node.ycoordinate)

        if nodetype == Junction:
            marker = 'o'
        elif nodetype == Reservoir:
            marker = 'D'
        elif nodetype == Tank:
            marker = 's'
        else:
            raise TypeError(f'A nodetype of either Junction, Reservoir or Tank was expected but a type {nodetype} '
                            f'was passed.')

        df = pd.DataFrame({'x': x,
                          'y': y},
                          index=nid)
        color = color[color.index.isin(df.index)]
        color.name = 'color'
        concat = pd.concat([df, color], axis=1, sort=True).fillna('k')
        concat['ms'] = ms

        if len(concat['color'].unique()) == 1 and 'k' in concat['color'].unique():
            pass
        elif nodetruncate:
            concat.loc[concat['color'] == 'k', 'ms'] = 0

        return plt.scatter(x=concat['x'], y=concat['y'], marker=marker, c=concat['color'], s=concat['ms'],
                           zorder=zorder, label='_nolegend_')


class Plotpipes:
    """ """

    def __new__(cls, network: Network, color):
        lines = []
        colors = []
        for pipe in get_pipes(network):
            lines.append(pipe.coordinates_2d.tolist())
            colors.append(color[pipe.id])
        lines = LineCollection(lines, color=colors)
        return lines


class Plotlink:
    """ """

    def __new__(cls, link: Union[Pipe, Pump, Valve], **kwargs):

        x1 = link.startnode.xcoordinate
        x2 = link.endnode.xcoordinate
        y1 = link.startnode.ycoordinate
        y2 = link.endnode.ycoordinate
        x = np.asarray([x1, x2])
        y = np.asarray([y1, y2])
        if isinstance(link, Pipe):
            return plt.plot(x, y, **kwargs)
        else:
            symbol = kwargs.pop('marker')
            return (plt.plot(x, y, marker=None, **kwargs), plt.plot(0.5 * (x1 + x2), 0.5 * (y1 + y2), marker=symbol, **kwargs))


class Plotgraph:
    """ """

    def __new__(cls, network: Network, fignum: Optional[int] = None):

        fig = plt.figure(fignum)
        nx.draw(network.graph)
        return fig


class Plotsimulation:
    """This function plots OOPNET networks with simulation results as a network plot with Matplotlib.
    
    Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.
    
    Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars in the middle, Pumps are plotted as lines with pentagons

    Args:
      network: OOPNET network object one wants to plot
      fignum: figure number, where to plot the network
      nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
      links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)). If links is None or specific links do not have  values, then the links are drawn as black lines
      colorbar: If True a colorbar is created, if False there is no colorbar in the plot. If one wants to set this setting for nodes and links seperatly, make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colorbar = {'node':True, 'link':False} plots a colorbar for nodes but not for links)
      colormap: Colormap defining which colors are used for the simulation results (default is matplotlib's colormap viridis). colormap can either be a string for matplotlib colormaps, a matplotlib.colors.LinearSegmentedColormap object or a matplotlib.colors.ListedColormap object. If one wants to use different colormaps for nodes and links, then make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colormaps = {'node':'jet', 'link':'cool'} plots nodes with colormap jet and links using colormap cool)
      ax: Matplotlib Axes object
      markersize: size of markers
      vlim: todo: add description
      robust: If True, 2nd and 98th percentiles are used as limits for the colorbar, else the minima and maxima are used.
      nodetruncate: If True, only junctions for which a value was submitted using the nodes parameter are plotted. If the nodes parameters isn't being used, all junctions are plotted. If not set True, junctions for which no value was submitted using the nodes parameters are plotted in black. This only applies to junctions and not to tanks and reservoirs, which are always plotted.

    Returns:
      Matplotlib's figure handle

    """

    def __new__(cls, network: Network, fignum: Optional[int] = None, nodes: Optional[pd.Series] = None,
                links: Optional[pd.Series] = None, colorbar: Union[bool, dict] = True,
                colormap: Union[str, dict] = 'viridis', ax: Optional[matplotlib.axes.Axes] = None,
                markersize: float = 8.0, robust: bool = False, vlim=None, nodetruncate=None):

        if isinstance(colormap, str):
            n_cmap = plt.get_cmap(colormap)
            l_cmap = plt.get_cmap(colormap)
        elif isinstance(colormap, (colors.LinearSegmentedColormap, colors.ListedColormap)):
            n_cmap = colormap
            l_cmap = colormap
        elif isinstance(colormap, dict):

            if 'node' in colormap:
                if isinstance(colormap['node'], str):
                    n_cmap = plt.get_cmap(colormap['node'])
                elif isinstance(colormap['node'], (colors.LinearSegmentedColormap, colors.ListedColormap)):
                    n_cmap = colormap['node']
            else:
                n_cmap = plt.get_cmap('jet')

            if 'link' in colormap:
                if isinstance(colormap['link'], str):
                    l_cmap = plt.get_cmap(colormap['link'])
                elif isinstance(colormap['link'], (colors.LinearSegmentedColormap, colors.ListedColormap)):
                    l_cmap = colormap['link']
            else:
                l_cmap = plt.get_cmap('jet')

        if ax:
            plt.sca(ax)
            fig = ax.get_figure()
        else:
            fig = plt.figure(fignum)
            ax = fig.add_subplot(111)

        # Nodes
        if nodes is None:
            nodelist = get_node_ids(network)
            nodecolors = pd.Series(['k'] * len(nodelist), index=nodelist)

        else:
            if vlim:
                vmin = vlim[0]
                vmax = vlim[1]
                extend = 'neither'

            elif robust:
                vmin = np.percentile(nodes.values, 2)
                vmax = np.percentile(nodes.values, 98)
                extend = 'both'
            else:
                vmin = np.nanmin(nodes.values)
                vmax = np.nanmax(nodes.values)
                extend = 'neither'
            cnorm = colors.Normalize(vmin=vmin, vmax=vmax)
            scalar_map = cmx.ScalarMappable(norm=cnorm, cmap=n_cmap)
            scalar_map._A = []
            nodecolors = nodes.apply(scalar_map.to_rgba)

            if (
                isinstance(colorbar, dict)
                and colorbar['node'] is True
                or not isinstance(colorbar, dict)
                and colorbar
            ):
                cb = plt.colorbar(scalar_map, extend=extend)
                cb.set_label(nodes.name, size=22)
                cb.ax.tick_params(labelsize=20)
        # Link
        if links is None:

            linklist = get_link_ids(network)
            linkcolors = pd.Series(['k'] * len(linklist), index=linklist)

        else:
            if vlim:
                vmin = vlim[0]
                vmax = vlim[1]
                extend = 'neither'

            elif robust:
                vmin = np.percentile(links.values, 2)
                vmax = np.percentile(links.values, 98)
                extend = 'both'
            else:
                vmin = np.nanmin(links.values)
                vmax = np.nanmax(links.values)
                extend = 'neither'
            cnorm = colors.Normalize(vmin=vmin, vmax=vmax)
            scalar_map = cmx.ScalarMappable(norm=cnorm, cmap=l_cmap)
            scalar_map._A = []
            linkcolors = links.apply(scalar_map.to_rgba)

            if (
                isinstance(colorbar, dict)
                and colorbar['link'] is True
                or not isinstance(colorbar, dict)
                and colorbar
            ):
                cb = plt.colorbar(scalar_map, extend=extend)
                cb.set_label(links.name, size=22)
                cb.ax.tick_params(labelsize=20)

        ax.add_collection(Plotpipes(network, color=linkcolors))

        list(map(lambda x: Plotlink(x, marker='v', color=outsidelist(x.id, linkcolors), ms=markersize), get_valves(network)))

        list(map(lambda x: Plotlink(x, marker='p', color=outsidelist(x.id, linkcolors), ms=markersize), get_pumps(network)))

        Plotnodes(get_junctions(network), nodetype=Junction, color=nodecolors, ms=4*markersize, zorder=3, nodetruncate=nodetruncate)

        Plotnodes(get_reservoirs(network), nodetype=Reservoir, color=nodecolors, ms=4*markersize, zorder=4)

        Plotnodes(get_tanks(network), nodetype=Tank, color=nodecolors, ms=4*markersize, zorder=5)

        plt.grid('off')
        plt.axis('equal')
        plt.axis('off')

        # return linkcolors
        return fig


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


class Plotnodetext:
    """ """

    def __new__(self, node: Union[Junction, Reservoir, Tank], text: str, **kwargs):
        return plt.text(node.xcoordinate, node.ycoordinate, text, **kwargs)


# class Plotsensors:
#
#     def __new__(self, network, fignum=None, sensors=None, text=None, **kwargs):
#         fig = plt.figure(fignum)
#         map(lambda x: Plotpipe(x, marker=None, color='k'), network.pipes)
#         map(lambda x: Plotjunction(x, **kwargs), sensors)
#         if text:
#             map(lambda x, y: Plotnodetext(x, y), sensors, text)
#         return fig


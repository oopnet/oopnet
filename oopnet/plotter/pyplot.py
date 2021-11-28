from matplotlib import pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from matplotlib.collections import LineCollection
import networkx as nx
import numpy as np
import pandas as pd
from traits.api import HasStrictTraits

from oopnet.elements.network import Pipe
from oopnet.utils.getters.element_lists import get_link_ids, get_node_ids

# todo: refactor
class Plotnodes(HasStrictTraits):
    """ """

    def __new__(self, nodes, nodetype, color, ms, zorder, nodetruncate=None):
        nid = []
        x = []
        y = []

        for node in nodes:
            nid.append(node.id)
            x.append(node.xcoordinate)
            y.append(node.ycoordinate)

        if nodetype == 'junction':
            marker = 'o'
        elif nodetype == 'reservoir':
            marker = 'D'
        elif nodetype == 'tank':
            marker = 's'

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

        return plt.scatter(x=concat['x'], y=concat['y'], marker=marker, c=concat['color'], s=concat['ms'], zorder=zorder, label='_nolegend_')


class Plotpipes(HasStrictTraits):
    """ """

    def __new__(self, network, color):

        lines = []
        pid = []

        for pipe in network.pipes:
            link = []

            ps = pipe.startnode
            pe = pipe.endnode

            s = (ps.xcoordinate, ps.ycoordinate)
            e = (pe.xcoordinate, pe.ycoordinate)

            link.append(s)
            link.append(e)

            lines.append(link)
            pid.append(pipe.id)

        df = pd.DataFrame(data=lines, index=pid)
        color = color[color.index.isin(df.index)]

        concat = pd.concat([df, color], axis=1, sort=True).fillna('k')
        lines = LineCollection(lines, color=concat.iloc[:, 2])

        return lines

class Plotlink(HasStrictTraits):
    """ """

    def __new__(self, link, **kwargs):

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


class Plotgraph(HasStrictTraits):
    """ """

    def __new__(self, network, fignum=None):

        fig = plt.figure(fignum)
        nx.draw(network.graph)
        return fig


class Plotsimulation(HasStrictTraits):
    """This function plots OOPNET networks with simulation results as a network plot with Matplotlib.
    
    Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.
    
    Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars in the middle, Pumps are plotted as lines with pentagons

    Args:
      network: OOPNET network object one wants to plot
      fignum: figure number, where to plot the network
      nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's Report functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
      links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's Report functions (e.g. Flow(rpt)). If links is None or specific links do not have  values, then the links are drawn as black lines
      colorbar: If True a colorbar is created, if False there is no colorbar in the plot. If one wants to set this setting for nodes and links seperatly, make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colorbar = {'node':True, 'link':False} plots a colorbar for nodes but not for links)
      colormap: Colormap defining which colors are used for the simulation results (default is matplotlib's colormap viridis). colormap can either be a string for matplotlib colormaps, a matplotlib.colors.LinearSegmentedColormap object or a matplotlib.colors.ListedColormap object. If one wants to use different colormaps for nodes and links, then make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colormaps = {'node':'jet', 'link':'cool'} plots nodes with colormap jet and links using colormap cool)
      robust: If True, 2nd and 98th percentiles are used as limits for the colorbar, else the minima and maxima are used.
      nodetruncate: If True, only junctions for which a value was submitted using the nodes parameter are plotted. If the nodes parameters isn't being used, all junctions are plotted. If not set True, junctions for which no value was submitted using the nodes parameters are plotted in black. This only applies to junctions and not to tanks and reservoirs, which are always plotted.

    Returns:
      Matplotlib's figure handle

    """

    def __new__(self, network, fignum=None, nodes=None, links=None, colorbar=True, colormap='viridis', ax=None, markersize=8.0, robust=False, vlim=None, nodetruncate=None):

        if isinstance(colormap, str):
            n_cmap = plt.get_cmap(colormap)
            l_cmap = plt.get_cmap(colormap)
        elif isinstance(colormap, colors.LinearSegmentedColormap) or isinstance(colormap, colors.ListedColormap):
            n_cmap = colormap
            l_cmap = colormap
        elif isinstance(colormap, dict):

            if 'node' in colormap:
                if isinstance(colormap['node'], str):
                    n_cmap = plt.get_cmap(colormap['node'])
                elif isinstance(colormap['node'], colors.LinearSegmentedColormap) or isinstance(colormap['node'], colors.ListedColormap):
                    n_cmap = colormap['node']
            else:
                n_cmap = plt.get_cmap('jet')

            if 'link' in colormap:
                if isinstance(colormap['link'], str):
                    l_cmap = plt.get_cmap(colormap['link'])
                elif isinstance(colormap['link'], colors.LinearSegmentedColormap)or isinstance(colormap['link'], colors.ListedColormap):
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
            if not vlim:
                if robust is True:
                    vmin = np.percentile(nodes.values, 2)
                    vmax = np.percentile(nodes.values, 98)
                    extend = 'both'
                else:
                    vmin = np.nanmin(nodes.values)
                    vmax = np.nanmax(nodes.values)
                    extend = 'neither'
            else:
                vmin = vlim[0]
                vmax = vlim[1]
                extend = 'neither'

            cnorm = colors.Normalize(vmin=vmin, vmax=vmax)
            scalar_map = cmx.ScalarMappable(norm=cnorm, cmap=n_cmap)
            scalar_map._A = []
            nodecolors = nodes.apply(scalar_map.to_rgba)

            if isinstance(colorbar, dict):
                if colorbar['node'] is True:
                    cb = plt.colorbar(scalar_map, extend=extend)
                    cb.set_label(nodes.name, size=22)
                    cb.ax.tick_params(labelsize=20)
            elif colorbar is True:
                cb = plt.colorbar(scalar_map, extend=extend)
                cb.set_label(nodes.name, size=22)
                cb.ax.tick_params(labelsize=20)
        # Link
        if links is None:

            linklist = get_link_ids(network)
            linkcolors = pd.Series(['k'] * len(linklist), index=linklist)

        else:
            if not vlim:
                if robust is True:
                    vmin = np.percentile(links.values, 2)
                    vmax = np.percentile(links.values, 98)
                    extend = 'both'
                else:
                    vmin = np.nanmin(links.values)
                    vmax = np.nanmax(links.values)
                    extend = 'neither'
            else:
                vmin = vlim[0]
                vmax = vlim[1]
                extend = 'neither'

            cnorm = colors.Normalize(vmin=vmin, vmax=vmax)
            scalar_map = cmx.ScalarMappable(norm=cnorm, cmap=l_cmap)
            scalar_map._A = []
            linkcolors = links.apply(scalar_map.to_rgba)

            if isinstance(colorbar, dict):
                if colorbar['link'] is True:
                    cb = plt.colorbar(scalar_map, extend=extend)
                    cb.set_label(links.name, size=22)
                    cb.ax.tick_params(labelsize=20)
            elif colorbar is True:
                    cb = plt.colorbar(scalar_map, extend=extend)
                    cb.set_label(links.name, size=22)
                    cb.ax.tick_params(labelsize=20)
        if network.pipes:
            ax.add_collection(Plotpipes(network, color=linkcolors))

        if network.valves:
            list(map(lambda x: Plotlink(x, marker='v', color=outsidelist(x.id, linkcolors), ms=markersize), network.valves))

        if network.pumps:
            list(map(lambda x: Plotlink(x, marker='p', color=outsidelist(x.id, linkcolors), ms=markersize), network.pumps))

        if network.junctions:
            Plotnodes(network.junctions, nodetype='junction', color=nodecolors, ms=4*markersize, zorder=3, nodetruncate=nodetruncate)

        if network.reservoirs:
            Plotnodes(network.reservoirs, nodetype='reservoir', color=nodecolors, ms=4*markersize, zorder=4)

        if network.tanks:
            Plotnodes(network.tanks, nodetype='tank', color=nodecolors, ms=4*markersize, zorder=5)

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


class Plotnodetext(HasStrictTraits):
    """ """

    def __new__(self, node, text, **kwargs):
        return plt.text(node.xcoordinate, node.ycoordinate, text, **kwargs)


# class Plotsensors(HasStrictTraits):
#
#     def __new__(self, network, fignum=None, sensors=None, text=None, **kwargs):
#         fig = plt.figure(fignum)
#         map(lambda x: Plotpipe(x, marker=None, color='k'), network.pipes)
#         map(lambda x: Plotjunction(x, **kwargs), sensors)
#         if text:
#             map(lambda x, y: Plotnodetext(x, y), sensors, text)
#         return fig


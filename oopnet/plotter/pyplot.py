from __future__ import annotations
from typing import Union, Optional, Type, TYPE_CHECKING
from functools import partial

import matplotlib.axes
from matplotlib import pyplot as plt
import matplotlib.colors as matplotlib_colors
import matplotlib.cm as cmx
from matplotlib.collections import LineCollection
from matplotlib.animation import FuncAnimation
import networkx as nx
import numpy as np
import pandas as pd

from oopnet.elements.network_components import (
    Junction,
    Reservoir,
    Tank,
    Pipe,
    Pump,
    Valve,
)
from oopnet.utils.getters.element_lists import (
    get_link_ids,
    get_node_ids,
    get_valves,
    get_pumps,
    get_junctions,
    get_reservoirs,
    get_tanks,
    get_pipes,
)

if TYPE_CHECKING:
    from oopnet.elements.network import Network
    from oopnet.elements.network_components import Link, Node


class NetworkPlotter:
    """Class for creating static matplotlib plots and matplotlib animations.

    Args:
      colorbar: If True a colorbar is created, if False there is no colorbar in the plot. If one wants to set this setting for nodes and links seperatly, make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colorbar = {'node':True, 'link':False} plots a colorbar for nodes but not for links)
      colormap: Colormap defining which colors are used for the simulation results (default is matplotlib's colormap viridis). colormap can either be a string for matplotlib colormaps, a matplotlib.colors.LinearSegmentedColormap object or a matplotlib.colors.ListedColormap object. If one wants to use different colormaps for nodes and links, then make use of a dictionary with key 'node' for nodes respectively key 'link' for links (e.g. colormaps = {'node':'jet', 'link':'cool'} plots nodes with colormap jet and links using colormap cool)
      truncate_nodes: If True, only junctions for which a value was submitted using the nodes parameter are plotted. If the nodes parameters isn't being used, all junctions are plotted. If not set True, junctions for which no value was submitted using the nodes parameters are plotted in black. This only applies to junctions and not to tanks and reservoirs, which are always plotted.
      robust: If True, 2nd and 98th percentiles are used as limits for the colorbar, else the minima and maxima are used.
      markersize: size of markers

    """

    _node_colormap = None
    _link_colormap = None

    def __init__(
        self,
        colorbar: Union[bool, dict] = True,
        colormap: Union[str, dict] = "viridis",
        truncate_nodes: bool = False,
        robust: bool = False,
        markersize: float = 8.0,
    ):
        self.colorbar = colorbar
        self.colormap = colormap
        self.truncate_nodes = truncate_nodes
        self.robust = robust
        self.markersize = markersize

    def _set_colormaps(self, colormap):
        n_cmap, l_cmap = None, None
        if isinstance(colormap, str):
            n_cmap = plt.get_cmap(colormap)
            l_cmap = plt.get_cmap(colormap)
        elif isinstance(
            colormap,
            (
                matplotlib_colors.LinearSegmentedColormap,
                matplotlib_colors.ListedColormap,
            ),
        ):
            n_cmap = colormap
            l_cmap = colormap
        elif isinstance(colormap, dict):
            if "node" in colormap:
                if isinstance(colormap["node"], str):
                    n_cmap = plt.get_cmap(colormap["node"])
                elif isinstance(
                    colormap["node"],
                    (
                        matplotlib_colors.LinearSegmentedColormap,
                        matplotlib_colors.ListedColormap,
                    ),
                ):
                    n_cmap = colormap["node"]
            else:
                n_cmap = plt.get_cmap("jet")

            if "link" in colormap:
                if isinstance(colormap["link"], str):
                    l_cmap = plt.get_cmap(colormap["link"])
                elif isinstance(
                    colormap["link"],
                    (
                        matplotlib_colors.LinearSegmentedColormap,
                        matplotlib_colors.ListedColormap,
                    ),
                ):
                    l_cmap = colormap["link"]
            else:
                l_cmap = plt.get_cmap("jet")
        else:
            raise ValueError(f"Cannot derive color maps from {colormap} object.")
        self._node_colormap = n_cmap
        self._link_colormap = l_cmap

    def _get_colorbar_limit(
        self, data: Union[pd.Series, pd.DataFrame], vlim: tuple[float, float]
    ):
        if not isinstance(data, (pd.Series, pd.DataFrame)):
            return

        perc = 2 if self.robust else 0

        if vlim:
            vmin = vlim[0]
            vmax = vlim[1]
            extend = "neither"
        elif self.robust:
            if isinstance(data, pd.DataFrame):
                vmin = np.percentile(data.min().values, perc)
                vmax = np.percentile(data.max().values, 100 - perc)
            else:
                vmin = np.percentile(data.values, 2)
                vmax = np.percentile(data.values, 98)
            extend = "both"
        else:
            vmin = data.min()
            vmax = data.max()
            if isinstance(data, pd.DataFrame):
                vmin = vmin.min()
                vmax = vmax.max()
            extend = "neither"
        return vmin, vmax, extend

    def _get_scalar_colormap(
        self, vlim: tuple[float, float, str], colormap
    ) -> pd.Series:
        import matplotlib.colors as colors

        normalized_colors = colors.Normalize(vmin=vlim[0], vmax=vlim[1])
        scalar_map = cmx.ScalarMappable(norm=normalized_colors, cmap=colormap)
        scalar_map._A = []
        return scalar_map

    def _add_colorbar(
        self, name: str, scalar_map, extend: str, ax: matplotlib.axes.Axes
    ):
        cb = plt.colorbar(scalar_map, extend=extend, ax=ax)
        cb.set_label(name, size=22)
        cb.ax.tick_params(labelsize=20)
        return matplotlib_colors

    # todo: refactor
    @staticmethod
    def _plot_single_node_type(
        ax: matplotlib.axes.Axes,
        nodes: list[Node],
        marker: str,
        colors: pd.Series,
        ms: Union[float, pd.Series],
        zorder: int,
        truncate_nodes: bool = False,
    ):
        node_ids = []
        x_coords = []
        y_coords = []

        for node in nodes:
            node_ids.append(node.id)
            x_coords.append(node.xcoordinate)
            y_coords.append(node.ycoordinate)

        coord_df = pd.DataFrame({"x": x_coords, "y": y_coords}, index=node_ids)
        select_colors = colors[colors.index.isin(node_ids)]
        select_colors.name = "color"
        node_plot_data = pd.concat([coord_df, select_colors], axis=1, sort=True).fillna(
            "k"
        )
        node_plot_data["ms"] = ms

        if (
            len(node_plot_data["color"].unique()) == 1
            and "k" in node_plot_data["color"].unique()
        ):
            pass
        elif truncate_nodes:
            node_plot_data.loc[node_plot_data["color"] == "k", "ms"] = 0

        return ax.scatter(
            x=node_plot_data["x"],
            y=node_plot_data["y"],
            marker=marker,
            c=node_plot_data["color"],
            s=node_plot_data["ms"],
            zorder=zorder,
            label="_nolegend_",
        )

    def _plot_single_link_type(
        self,
        ax: matplotlib.axes.Axes,
        links: list[Link],
        colors: pd.Series,
        ms: Union[float, pd.Series],
        zorder: int,
        line_width: Union[float, pd.Series, None],
        marker: Optional[str] = None,
    ):
        link_ids = []
        line_coords = []

        for link in links:
            link_ids.append(link.id)
            line_coords.append(link.coordinates_2d.tolist())

        select_colors = colors[colors.index.isin(link_ids)].fillna("k")
        select_colors.name = "color"

        if isinstance(line_width, pd.Series):
            select_line_width = line_width[line_width.index.isin(link_ids)].values
        elif isinstance(line_width, float):
            select_line_width = [line_width] * len(link_ids)
        else:
            select_line_width = [1.5] * len(link_ids)

        col = LineCollection(
            line_coords, color=select_colors, linewidths=select_line_width
        )
        ax.add_collection(col)

        if marker:
            centers = [x.center for x in links]
            return ax.scatter(
                x=[coords[0] for coords in centers],
                y=[coords[1] for coords in centers],
                marker=marker,
                c=select_colors,
                s=ms,
                zorder=zorder,
                label="_nolegend_",
            )

    def _plot_links(
        self,
        network: Network,
        ax: matplotlib.axes.Axes,
        colors: pd.Series,
        link_width: Union[float, pd.Series, None],
    ):
        if isinstance(link_width, pd.Series):
            link_width = link_width / link_width.max() * 5
        elif isinstance(link_width, float):
            link_width = pd.Series(index=get_link_ids(network), data=None)

        # plot pipes without marker
        self._plot_single_link_type(
            ax=ax,
            links=get_pipes(network),
            marker=None,
            colors=colors,
            ms=4 * self.markersize,
            zorder=3,
            line_width=link_width,
        )
        # plot pumps with pentagon marker
        self._plot_single_link_type(
            ax=ax,
            links=get_pumps(network),
            marker="p",
            colors=colors,
            ms=4 * self.markersize,
            zorder=3,
            line_width=link_width,
        )
        # plot pipes without down-facing triangle marker
        self._plot_single_link_type(
            ax=ax,
            links=get_valves(network),
            marker="v",
            colors=colors,
            ms=4 * self.markersize,
            zorder=3,
            line_width=link_width,
        )

    @staticmethod
    def _prepare_plot(ax: Optional[matplotlib.axes.Axes], fignum: Optional[int]):
        if ax:
            fig = ax.get_figure()
        else:
            fig = plt.figure(fignum)
            ax = fig.add_subplot(111)
        plt.grid(False)
        plt.axis("equal")
        plt.axis("off")
        return fig, ax

    def _plot_nodes(
        self, network: Network, ax: matplotlib.axes.Axes, colors: pd.Series
    ):
        # plot junctions with circle marker
        self._plot_single_node_type(
            ax=ax,
            nodes=get_junctions(network),
            marker="o",
            colors=colors,
            ms=4 * self.markersize,
            zorder=3,
            truncate_nodes=self.truncate_nodes,
        )
        # plot tanks with diamond marker
        self._plot_single_node_type(
            ax=ax,
            nodes=get_tanks(network),
            marker="D",
            colors=colors,
            ms=4 * self.markersize,
            zorder=4,
            truncate_nodes=False,
        )
        # plot reservoirs with square marker
        self._plot_single_node_type(
            ax=ax,
            nodes=get_reservoirs(network),
            marker="s",
            colors=colors,
            ms=4 * self.markersize,
            zorder=5,
            truncate_nodes=False,
        )

    def plot(
        self,
        network: Network,
        fignum: Optional[int] = None,
        nodes: Optional[pd.Series] = None,
        links: Optional[pd.Series] = None,
        link_width: Optional[pd.Series] = None,
        ax: Optional[matplotlib.axes.Axes] = None,
        nodes_vlim: Optional[tuple[float, float]] = None,
        links_vlim: Optional[tuple[float, float]] = None,
    ):
        """This function plots OOPNET networks with simulation results as a network plot with Matplotlib.

        Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.

        Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars in the middle, Pumps are plotted as lines with pentagons

        Args:
          network: OOPNET network object one wants to plot
          fignum: figure number, where to plot the network
          nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
          nodes_vlim:
          links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)). If links is None or specific links do not have  values, then the links are drawn as black lines
          links_vlim:
          link_width: Values describing the link width as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)).
          ax: Matplotlib Axes object

        Returns:
          Matplotlib's figure handle

        """
        self._set_colormaps(self.colormap)
        fig, ax = self._prepare_plot(ax=ax, fignum=fignum)

        # get Link colors
        links_vlim = self._get_colorbar_limit(data=links, vlim=links_vlim)
        if links is None:
            link_ids = get_link_ids(network)
            link_colors = pd.Series(["k"] * len(link_ids), index=link_ids)
            link_scalar_map = None
        else:
            link_scalar_map = self._get_scalar_colormap(
                vlim=links_vlim, colormap=self._node_colormap
            )
            link_colors = links.apply(link_scalar_map.to_rgba)

        link_colorbar = (
            isinstance(self.colorbar, dict)
            and self.colorbar["link"] is True
            or isinstance(self.colorbar, bool)
            and self.colorbar
        ) and links is not None
        if link_colorbar:
            self._add_colorbar(links.name, link_scalar_map, links_vlim[2], ax=ax)

        # get Node colors
        nodes_vlim = self._get_colorbar_limit(nodes, nodes_vlim)
        if nodes is None:
            node_ids = get_node_ids(network)
            node_colors = pd.Series(["k"] * len(node_ids), index=node_ids)
            node_scalar_map = None
        else:
            node_scalar_map = self._get_scalar_colormap(
                vlim=nodes_vlim, colormap=self._node_colormap
            )
            node_colors = nodes.apply(node_scalar_map.to_rgba)

        node_colorbar = (
            isinstance(self.colorbar, dict)
            and self.colorbar["node"] is True
            or isinstance(self.colorbar, bool)
            and self.colorbar
        ) and nodes is not None
        if node_colorbar:
            self._add_colorbar(nodes.name, node_scalar_map, nodes_vlim[2], ax=ax)

        self._plot_nodes(network=network, ax=ax, colors=node_colors)
        self._plot_links(
            network=network, ax=ax, colors=link_colors, link_width=link_width
        )
        return fig

    def _render_animation_frame(
        self,
        time,
        ax: matplotlib.axes.Axes,
        network: Network,
        node_colors: pd.DataFrame,
        link_colors: pd.DataFrame,
        link_width: Optional[pd.DataFrame],
    ):
        ax.clear()
        node_data = (
            node_colors.loc[time]
            if isinstance(node_colors, pd.DataFrame)
            else node_colors
        )
        link_data = (
            link_colors.loc[time]
            if isinstance(link_colors, pd.DataFrame)
            else link_colors
        )
        link_width_data = (
            link_width.loc[time] if isinstance(link_width, pd.DataFrame) else link_width
        )
        self._plot_nodes(network=network, ax=ax, colors=node_data)
        self._plot_links(
            network=network, ax=ax, colors=link_data, link_width=link_width_data
        )

    def animate(
        self,
        network: Network,
        fignum: Optional[int] = None,
        ax: Optional[matplotlib.axes.Axes] = None,
        nodes: Optional[pd.DataFrame] = None,
        node_label: Optional[str] = None,
        links: Optional[pd.DataFrame] = None,
        link_label: Optional[str] = None,
        link_width: Optional[pd.DataFrame] = None,
        interval: int = 500,
        repeat: bool = False,
        nodes_vlim: Optional[tuple[float, float]] = None,
        links_vlim: Optional[tuple[float, float]] = None,
    ) -> FuncAnimation:
        """This function plots OOPNET networks with simulation results as a network plot with Matplotlib.

        Symbols for Nodes: Junctions are plotted as circles, Reservoirs as diamonds, Tanks as squares.

        Symbols for Links: Pipes are plotted as lines with no markers, Valves are plotted as lines with triangulars in the middle, Pumps are plotted as lines with pentagons

        Args:
          network: OOPNET network object one wants to plot
          fignum: figure number, where to plot the network
          nodes: Values related to the nodes as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Pressure(rpt)). If nodes is None or specific nodes do not have  values, then the nodes are drawn as black circles
          nodes_vlim:
          links: Values related to the links as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)). If links is None or specific links do not have  values, then the links are drawn as black lines
          links_vlim:
          link_width: Values describing the link width as Pandas Series generated e.g. by one of OOPNET's SimulationReport functions (e.g. Flow(rpt)).
          ax: Matplotlib Axes object

        Returns:
          Matplotlib's figure handle

        """
        self._set_colormaps(self.colormap)
        fig, ax = self._prepare_plot(ax=ax, fignum=fignum)

        # get Link colors
        links_vlim = self._get_colorbar_limit(data=links, vlim=links_vlim)
        if links is None:
            link_ids = get_link_ids(network)
            link_colors = pd.Series(["k"] * len(link_ids), index=link_ids)
            link_scalar_map = None
        else:
            link_scalar_map = self._get_scalar_colormap(
                vlim=links_vlim, colormap=self._node_colormap
            )
            link_colors = links.applymap(link_scalar_map.to_rgba)

        link_colorbar = (
            isinstance(self.colorbar, dict)
            and self.colorbar["link"] is True
            or isinstance(self.colorbar, bool)
            and self.colorbar
        ) and links is not None
        if link_colorbar:
            self._add_colorbar(link_label, link_scalar_map, links_vlim[2], ax=ax)

        # get Node colors
        nodes_vlim = self._get_colorbar_limit(nodes, nodes_vlim)
        if nodes is None:
            node_ids = get_node_ids(network)
            node_colors = pd.Series(["k"] * len(node_ids), index=node_ids)
            node_scalar_map = None
        else:
            node_scalar_map = self._get_scalar_colormap(
                vlim=nodes_vlim, colormap=self._node_colormap
            )
            node_colors = nodes.applymap(node_scalar_map.to_rgba)

        node_colorbar = (
            isinstance(self.colorbar, dict)
            and self.colorbar["node"] is True
            or isinstance(self.colorbar, bool)
            and self.colorbar
        ) and nodes is not None
        if node_colorbar:
            self._add_colorbar(node_label, node_scalar_map, nodes_vlim[2], ax=ax)

        if isinstance(nodes, pd.DataFrame):
            times = nodes.index
        elif isinstance(links, pd.DataFrame):
            times = links.index
        elif isinstance(link_width, pd.DataFrame):
            times = link_width.index
        else:
            raise ValueError(
                "A pandas DataFrame must be provided for at least one of these arguments: nodes, links, linkwidth"
            )
        fun = partial(
            self._render_animation_frame,
            ax=ax,
            link_colors=link_colors,
            node_colors=node_colors,
            link_width=link_width,
            network=network,
        )
        anim = FuncAnimation(fig, fun, frames=times, interval=interval, repeat=repeat)

        # remove border around plot
        ax.set_frame_on(False)

        # remove ticks on x- and y-axis
        plt.tick_params(
            axis="both",  # changes apply to the x-axis
            which="both",  # both major and minor ticks are affected
            bottom=False,  # ticks along the bottom edge are off
            left=False,  # ticks along the top edge are off
            labelbottom=False,  # labels along the bottom edge are off
            labelleft=False,
        )  # labels along the left edge are off
        return anim

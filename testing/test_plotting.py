import unittest

from matplotlib import pyplot as plt

from oopnet.plotter.pyplot import Plotsimulation
from oopnet.utils.getters.property_getters import get_diameter

from testing.base import ETownModel, CTownModel


class ETownModelPlottingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ETownModel()

    def test_default_plot(self):
        fig = Plotsimulation(self.model.network)
        self.assertIsInstance(fig, plt.Figure)


class CTownModelPlottingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = CTownModel()
        self.rpt = self.model.network.run()

    def test_links_nodes_plot(self):
        self.model.network.plot(links=self.rpt.flow, nodes=self.rpt.pressure, )

    def test_colorbar_plot(self):
        self.model.network.plot(links=self.rpt.flow, nodes=self.rpt.pressure, colorbar=True)
        self.model.network.plot(links=self.rpt.flow, nodes=self.rpt.pressure, colorbar=False)

    def test_robust_colorbar_plot(self):
        self.model.network.plot(links=self.rpt.flow, nodes=self.rpt.pressure, robust=True)

    def test_linkwidth_plot(self):
        dn = get_diameter(self.model.network)
        self.model.network.plot(linkwidth=dn)

    def test_nodetruncate_plot(self):
        p = self.rpt.pressure.iloc[:100]
        self.model.network.plot(nodes=p, nodetruncate=True)

    def test_different_colormaps_plot(self):
        self.model.network.plot(nodes=self.rpt.pressure,
                                links=self.rpt.flow,
                                colormap={'node': 'jet', 'link': 'cool'})

    def test_existing_ax_plot(self):
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots()
        self.model.network.plot(ax=ax)

    def test_different_markersize_plot(self):
        self.model.network.plot(markersize=2)


if __name__ == '__main__':
    unittest.main()

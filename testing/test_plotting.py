import unittest

from matplotlib import pyplot as plt

from oopnet.plotter.pyplot import Plotsimulation
from base import ETownModel


class ETownModelPlottingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ETownModel()

    def test_default_plot(self):
        fig = Plotsimulation(self.model.network)
        self.assertIsInstance(fig, plt.Figure)


if __name__ == '__main__':
    unittest.main()

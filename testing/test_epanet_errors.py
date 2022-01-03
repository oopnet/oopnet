import unittest

from oopnet.api import Run
from oopnet.elements.network import Network
from oopnet.elements.network_components import Tank, Junction
from oopnet.utils.adders import add_junction, add_tank
from oopnet.utils.getters import get_pipe, get_junction, get_tank
from testing.base import create_dummy_spa_network


# todo: fix and expand
class BlankSimulationErrorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = Network()

    def test_not_enough_nodes(self):
        from oopnet.report.simulation_errors import NotEnoughNodesError
        with self.assertRaises(NotEnoughNodesError):
            Run(self.network)

    def test_not_enough_sources(self):
        from oopnet.report.simulation_errors import NotEnoughSourcesError
        add_junction(self.network, Junction(id='test'))
        with self.assertRaises(NotEnoughSourcesError):
            Run(self.network)

    def test_node_not_connected(self):
        from oopnet.report.simulation_errors import UnconnectedNodeError
        add_tank(self.network, Tank('tank'))
        add_junction(self.network, Junction('junction'))
        with self.assertRaises(UnconnectedNodeError):
            Run(self.network)

class ExistingModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = create_dummy_spa_network()

    def test_illegal_node_property(self):
        from oopnet.report.simulation_errors import EPANETSimulationError
        t = get_tank(self.network, 'T-1')
        t.diam = -100
        with self.assertRaises(EPANETSimulationError) as e:
            Run(self.network)
            self.assertTrue('IllegalNodePropertyError' in e.args[0])

    def test_illegal_link_property(self):
        from oopnet.report.simulation_errors import IllegalLinkPropertyError
        j = get_pipe(self.network, 'P-1')
        j.diameter = -100
        with self.assertRaises(IllegalLinkPropertyError):
            Run(self.network)


if __name__ == '__main__':
    unittest.main()

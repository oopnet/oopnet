import unittest

from oopnet.elements.network import Network
from oopnet.elements.network_components import Tank, Junction
from oopnet.elements.system_operation import Curve
from oopnet.utils.adders import add_junction, add_tank, add_curve
from oopnet.utils.getters import get_pipe, get_tank
from oopnet.report.simulation_errors import EPANETSimulationError
from testing.base import create_dummy_spa_network


# todo: fix and expand
class BlankSimulationErrorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = Network()

    def test_not_enough_nodes(self):
        from oopnet.report.simulation_errors import NotEnoughNodesError
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(NotEnoughNodesError in e.errors)

    def test_not_enough_sources(self):
        from oopnet.report.simulation_errors import NotEnoughSourcesError
        add_junction(self.network, Junction(id='test'))
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(NotEnoughSourcesError in e.arrors)

    def test_invalid_curve(self):
        from oopnet.report.simulation_errors import InvalidCurveError
        add_curve(self.network, Curve(id='curve', xvalues=[3, 2, 1], yvalues=[1, 2, 3]))
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(InvalidCurveError in e.errors)


class ExistingModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = create_dummy_spa_network()

    def test_node_not_connected(self):
        from oopnet.report.simulation_errors import UnconnectedNodeError
        add_tank(self.network, Tank('tank'))
        add_junction(self.network, Junction('junction'))
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(UnconnectedNodeError in e.errors)

    def test_illegal_node_property(self):
        from oopnet.report.simulation_errors import IllegalNodePropertyError
        t = get_tank(self.network, 'T-1')
        t.diam = -100
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(IllegalNodePropertyError in e.errors)

    def test_illegal_link_property(self):
        from oopnet.report.simulation_errors import IllegalLinkPropertyError
        j = get_pipe(self.network, 'P-1')
        j.diameter = -100
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(IllegalLinkPropertyError in e.errors)

    def test_too_many_characters(self):
        from oopnet.report.simulation_errors import TooManyCharactersError
        j = get_pipe(self.network, 'P-1')
        j.id = 300 * 'a'
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run()
            self.assertTrue(TooManyCharactersError in e.errors)

    def test_id_duplicate(self):
        from oopnet.report.simulation_errors import SharedIDError

if __name__ == '__main__':
    unittest.main()

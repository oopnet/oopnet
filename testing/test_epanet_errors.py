import unittest

from oopnet.elements.network import Network
from oopnet.elements.network_components import Tank, Junction
from oopnet.elements.system_operation import Curve
from oopnet.utils.adders import add_junction, add_tank, add_curve
from oopnet.utils.getters import get_pipe, get_tank, get_pump
from oopnet.simulator.simulation_errors import EPANETSimulationError

from testing.base import create_dummy_spa_network


# todo: fix and expand
class BlankSimulationErrorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = Network()

    def _check_exception_raised(self, error):
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run(output=True)
        self.assertTrue(e.exception.check_contained_errors(error))

    def test_not_enough_nodes(self):
        from oopnet.simulator.simulation_errors import NotEnoughNodesError
        self._check_exception_raised(NotEnoughNodesError)

    def test_not_enough_sources(self):
        from oopnet.simulator.simulation_errors import NotEnoughSourcesError
        add_junction(self.network, Junction(id='test'))
        self._check_exception_raised(NotEnoughSourcesError)


class ExistingModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = create_dummy_spa_network()

    def _check_exception_raised(self, error):
        with self.assertRaises(EPANETSimulationError) as e:
            self.network.run(output=True)
        self.assertTrue(e.exception.check_contained_errors(error))

    def test_node_not_connected(self):
        from oopnet.simulator.simulation_errors import UnconnectedNodeError
        add_tank(self.network, Tank('tank'))
        add_junction(self.network, Junction('junction'))
        self._check_exception_raised(UnconnectedNodeError)

    def test_illegal_node_property(self):
        from oopnet.simulator.simulation_errors import IllegalNodePropertyError
        t = get_tank(self.network, 'T-1')
        t.diameter = -100
        self._check_exception_raised(IllegalNodePropertyError)

    def test_illegal_link_property(self):
        from oopnet.simulator.simulation_errors import IllegalLinkPropertyError
        j = get_pipe(self.network, 'P-1')
        j.diameter = -100
        self._check_exception_raised(IllegalLinkPropertyError)

    def test_invalid_curve(self):
        from oopnet.simulator.simulation_errors import InvalidPumpError
        c = Curve(id='curve', xvalues=[3, 2, 1], yvalues=[1, 2, 3])
        add_curve(self.network, c)
        p = get_pump(self.network, 'PU-1')
        p.head = c
        self._check_exception_raised(InvalidPumpError)

    def test_too_many_characters(self):
        from oopnet.simulator.simulation_errors import InvalidIDError
        j = get_pipe(self.network, 'P-1')
        j.id = 50 * 'a'
        self._check_exception_raised(InvalidIDError)

    def test_id_duplicate(self):
        pass

if __name__ == '__main__':
    unittest.main()

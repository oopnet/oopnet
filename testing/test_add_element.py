import unittest

from oopnet.elements.network import Network
from oopnet.elements.network_components import Junction, Reservoir, Tank, Pipe, Pump, Valve, Link, Node, TCV
from oopnet.elements.system_operation import Pattern, Curve
from oopnet.elements.component_registry import ComponentExistsError
from oopnet.utils.getters import *
from oopnet.utils.adders import *

from testing.base import add_dummy_junctions, create_dummy_spa_network


class BlankModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = Network()

    def test_add_simple_junction_object(self):
        add_junction(self.network, Junction(id='test', xcoordinate=1, ycoordinate=2, elevation=3, initialquality=0.1,
                                            sourcequality=0.2, demand=10, comment='Test', emittercoefficient=0.2))
        self.assertEqual(1, len(self.network._nodes['junctions']))
        j = get_junction(self.network, 'test')
        self.assertEqual(1, j.xcoordinate)

    def test_add_simple_reservoir_object(self):
        add_reservoir(self.network, Reservoir(id='test', xcoordinate=1, ycoordinate=2, initialquality=0.1,
                                              sourcequality=0.2, head=10, comment='Test'))
        self.assertEqual(1, len(self.network._nodes['reservoirs']))
        r = get_reservoir(self.network, 'test')
        self.assertEqual(1, r.xcoordinate)

    def test_add_simple_tank_object(self):
        add_tank(self.network, Tank(id='test', xcoordinate=1, ycoordinate=2, elevation=3, initialquality=0.1,
                                    sourcequality=0.2, comment='Test', initlevel=0.3, maxlevel=2.0, minlevel=0.1,
                                    minvolume=1.0))
        self.assertEqual(1, len(self.network._nodes['tanks']))
        t = get_tank(self.network, 'test')
        self.assertEqual(1, t.xcoordinate)

    def test_add_simple_pattern_object(self):
        add_pattern(self.network, Pattern(id='test', multipliers=[15, 10]))
        self.assertEqual(1, len(self.network._patterns))
        p = get_pattern(self.network, 'test')
        self.assertEqual([15, 10], p.multipliers)

    def test_add_simple_curve_object(self):
        add_curve(self.network, Curve(id='test', xvalues=[15, 10], yvalues=[10, 15]))
        self.assertEqual(1, len(self.network._curves))
        p = get_curve(self.network, 'test')
        self.assertEqual([15, 10], p.xvalues)


class BlankModelLinkTest(unittest.TestCase):
    def setUp(self) -> None:
        network = Network()
        self.network = add_dummy_junctions(network, 2)

    def test_add_simple_pipe_object(self):
        j1 = get_junction(self.network, 'J-1')
        j2 = get_junction(self.network, 'J-2')
        add_pipe(self.network, Pipe(id='test', startnode=j1, endnode=j2, diameter=200, length=250, roughness=0.3,
                                    minorloss=1.0, status='CLOSED', comment='Test'))
        self.assertEqual(1, len(self.network._links['pipes']))
        p = get_pipe(self.network, 'test')
        self.assertEqual('CLOSED', p.status)

    def test_add_simple_pump_object(self):
        j1 = get_junction(self.network, 'J-1')
        j2 = get_junction(self.network, 'J-2')
        add_pump(self.network, Pump(id='test', startnode=j1, endnode=j2, power=100, comment='Test'))
        self.assertEqual(1, len(self.network._links['pumps']))
        p = get_pump(self.network, 'test')
        self.assertEqual(100, p.power)

    def test_add_simple_valve_object(self):
        j1 = get_junction(self.network, 'J-1')
        j2 = get_junction(self.network, 'J-2')
        add_valve(self.network, TCV(id='test', startnode=j1, endnode=j2, diameter=150, minorloss=1.0,
                                      comment='Test'))
        self.assertEqual(1, len(self.network._links['valves']))
        v = get_valve(self.network, 'test')
        self.assertEqual(150, v.diameter)


class ExistingModelTest(unittest.TestCase):
    def setUp(self) -> None:
        self.network = create_dummy_spa_network()

    # todo: add tests that include patterns + curves

    def test_add_existing_junction(self):
        with self.assertRaises(ComponentExistsError):
            add_junction(self.network, Junction(id='J-1'))

    def test_add_existing_reservoir(self):
        with self.assertRaises(ComponentExistsError):
            add_reservoir(self.network, Reservoir(id='R-1'))

    def test_add_existing_tank(self):
        with self.assertRaises(ComponentExistsError):
            add_tank(self.network, Tank(id='T-1'))

    def test_add_existing_pipe(self):
        with self.assertRaises(ComponentExistsError):
            add_pipe(self.network, Pipe(id='P-1'))

    def test_add_existing_pump(self):
        with self.assertRaises(ComponentExistsError):
            add_pump(self.network, Pump(id='PU-1'))

    def test_add_existing_valve(self):
        with self.assertRaises(ComponentExistsError):
            add_valve(self.network, Valve(id='V-1'))

    def test_invalid_node(self):
        with self.assertRaises(TypeError):
            add_node(self.network, Pipe(id='1'))

    def test_invalid_link(self):
        with self.assertRaises(TypeError):
            add_link(self.network, Junction(id='1'))

    def test_add_component_twice(self):
        from copy import deepcopy
        net1 = self.network
        net2 = deepcopy(self.network)
        j = Junction(id='test')
        add_junction(net1, j)
        with self.assertRaises(RuntimeError):
            add_junction(net2, j)


if __name__ == '__main__':
    unittest.main()

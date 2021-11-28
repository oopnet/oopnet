import unittest

from oopnet.utils.getters import *

from testing.base import SimpleModel


class SimpleDeepcopyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()
        self.old_network = self.model.network
        self.new_network = self.model.network.__deepcopy__()

    def test_junction(self):       
        junction_old = get_junction(self.old_network, 'J-1')
        junction_new = get_junction(self.new_network, 'J-1')
        junction_old.demand = 1
        self.assertEqual(1, junction_old.demand)
        self.assertEqual(10, junction_new.demand)
        
    def test_tank(self):
        tank_old = get_tank(self.old_network, 'T-1')
        tank_new = get_tank(self.new_network, 'T-1')
        tank_old.diam = 1
        self.assertEqual(1, tank_old.diam)
        self.assertEqual(50, tank_new.diam)
    
    def test_reservoir(self):
        reservoir_old = get_reservoir(self.old_network, 'R-1')
        reservoir_new = get_reservoir(self.new_network, 'R-1')
        reservoir_old.head = 1
        self.assertEqual(1, reservoir_old.head)
        self.assertEqual(50, reservoir_new.head)

    def test_pipe(self):
        pipe_old = get_pipe(self.old_network, 'P-1')
        pipe_new = get_pipe(self.new_network, 'P-1')
        pipe_old.diameter = 100
        self.assertEqual(100, pipe_old.diameter)
        self.assertEqual(200, pipe_new.diameter)
        
    def test_pump(self):
        pump_old = get_pump(self.old_network, 'PU-1')
        pump_new = get_pump(self.new_network, 'PU-1')
        pump_old.value = 100
        self.assertEqual(100, pump_old.value)
        self.assertEqual('C-1', pump_new.value)
    
    def test_valve(self):
        valve_old = get_valve(self.old_network, 'V-1')
        valve_new = get_valve(self.new_network, 'V-1')
        valve_old.diameter = 1
        self.assertEqual(1, valve_old.diameter)
        self.assertEqual(12, valve_new.diameter)
        

if __name__ == '__main__':
    unittest.main()

import datetime
import unittest
from copy import deepcopy

from oopnet.utils.getters import *

from testing.base import SimpleModel


class SimpleDeepcopyTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()
        self.old_network = self.model.network
        self.new_network = deepcopy(self.model.network)

    def test_junction(self):
        junction_old = get_junction(self.old_network, 'J-1')
        junction_new = get_junction(self.new_network, 'J-1')
        junction_old.demand = 1
        self.assertFalse(junction_old.demand == junction_new.demand)

    def test_tank(self):
        tank_old = get_tank(self.old_network, 'T-1')
        tank_new = get_tank(self.new_network, 'T-1')
        tank_old.diam = 1
        self.assertFalse(tank_old.diam == tank_new.diam)

    def test_reservoir(self):
        reservoir_old = get_reservoir(self.old_network, 'R-1')
        reservoir_new = get_reservoir(self.new_network, 'R-1')
        reservoir_old.head = 1
        self.assertFalse(reservoir_old.head == reservoir_new.head)

    def test_pipe(self):
        pipe_old = get_pipe(self.old_network, 'P-1')
        pipe_new = get_pipe(self.new_network, 'P-1')
        pipe_old.diameter = 100
        self.assertFalse(pipe_old.diameter == pipe_new.diameter)

    def test_pump(self):
        pump_old = get_pump(self.old_network, 'PU-1')
        pump_new = get_pump(self.new_network, 'PU-1')
        pump_old.power = 100
        self.assertFalse(pump_old.power == pump_new.power)

    def test_valve(self):
        valve_old = get_valve(self.old_network, 'V-1')
        valve_new = get_valve(self.new_network, 'V-1')
        valve_old.diameter = 1
        self.assertFalse(valve_old.diameter == valve_new.diameter)

    def test_options(self):
        old_options = self.old_network.options
        new_options = self.new_network.options
        old_options.demandmodel = 'PDA'
        self.assertFalse(old_options == new_options)

    def test_times(self):
        old_times = self.old_network.times
        new_times = self.new_network.times
        old_times.duration = datetime.timedelta(hours=2)
        self.assertFalse(old_times == new_times)

    def test_report_parameter(self):
        old_parameter = self.old_network.reportparameter
        new_parameter = self.new_network.reportparameter
        old_parameter.demand = 'NO'
        self.assertFalse(old_parameter == new_parameter)

    def test_report_precision(self):
        old_precision = self.old_network.reportprecision
        new_precision = self.new_network.reportprecision
        old_precision.demand = 4
        self.assertFalse(old_precision == new_precision)

    def test_report(self):
        old_report = self.old_network.report
        new_report = self.new_network.report
        old_report.status = 'YES'
        self.assertFalse(old_report == new_report)
        

if __name__ == '__main__':
    unittest.main()

import datetime
import unittest
from copy import deepcopy

from oopnet.elements.network import Network
from oopnet.utils.getters import *

from testing.base import SimpleModel, PatternCurveModel


class DeepcopyTest(unittest.TestCase):
    def compare_junctions(self, old_network: Network, new_network: Network):
        j_old = get_junctions(old_network)
        j_new = get_junctions(new_network)
        self.assertEqual(j_old, j_new)

    def compare_tanks(self, old_network: Network, new_network: Network):
        t_old = get_tanks(old_network)
        t_new = get_tanks(new_network)
        self.assertEqual(t_old, t_new)

    def compare_reservoirs(self, old_network: Network, new_network: Network):
        r_old = get_reservoirs(old_network)
        r_new = get_reservoirs(new_network)
        self.assertEqual(r_old, r_new)

    def compare_pipes(self, old_network: Network, new_network: Network):
        p_old = get_pipes(old_network)
        p_new = get_pipes(new_network)
        self.assertEqual(p_old, p_new)

    def compare_pumps(self, old_network: Network, new_network: Network):
        pu_old = get_pumps(old_network)
        pu_new = get_pumps(new_network)
        self.assertEqual(pu_old, pu_new)

    def compare_valves(self, old_network: Network, new_network: Network):
        v_old = get_valves(old_network)
        v_new = get_valves(new_network)
        self.assertEqual(v_old, v_new)
        
    def compare_options(self, old_network: Network, new_network: Network):
        opt_old = old_network.options
        opt_new = new_network.options
        self.assertEqual(opt_old, opt_new)
        
    def compare_times(self, old_network: Network, new_network: Network):
        ti_old = old_network.times
        ti_new = new_network.times
        self.assertEqual(ti_old, ti_new)
        
    def compare_reportparameters(self, old_network: Network, new_network: Network):
        param_old = old_network.reportparameter
        param_new = new_network.reportparameter
        self.assertEqual(param_old, param_new)

    def compare_reportprecision(self, old_network: Network, new_network: Network):
        prec_old = old_network.reportprecision
        prec_new = new_network.reportprecision
        self.assertEqual(prec_old, prec_new)
        
    def compare_report(self, old_network: Network, new_network: Network):
        rpt_old = old_network.report
        rpt_new = new_network.report
        self.assertEqual(rpt_old, rpt_new)

    def compare_patterns(self, old_network: Network, new_network: Network):
        pat_old = get_patterns(old_network)
        pat_new = get_patterns(new_network)
        self.assertEqual(pat_old, pat_new)

    def compare_curves(self, old_network: Network, new_network: Network):
        c_old = get_curves(old_network)
        c_new = get_curves(new_network)
        self.assertEqual(c_old, c_new)


class SimpleDeepcopyTest(DeepcopyTest):
    def setUp(self) -> None:
        self.model = SimpleModel()
        self.old_network = self.model.network
        self.new_network = deepcopy(self.model.network)

    def test_junction(self):
        self.compare_junctions(self.old_network, self.new_network)
        junction_old = get_junction(self.old_network, 'J-1')
        junction_new = get_junction(self.new_network, 'J-1')
        junction_old.demand = 1
        self.assertFalse(junction_old.demand == junction_new.demand)

    def test_tank(self):
        self.compare_tanks(self.old_network, self.new_network)
        tank_old = get_tank(self.old_network, 'T-1')
        tank_new = get_tank(self.new_network, 'T-1')
        tank_old.diameter = 1
        self.assertFalse(tank_old.diameter == tank_new.diameter)

    def test_reservoir(self):
        self.compare_reservoirs(self.old_network, self.new_network)
        reservoir_old = get_reservoir(self.old_network, 'R-1')
        reservoir_new = get_reservoir(self.new_network, 'R-1')
        reservoir_old.head = 1
        self.assertFalse(reservoir_old.head == reservoir_new.head)

    def test_pipe(self):
        self.compare_pipes(self.old_network, self.new_network)
        pipe_old = get_pipe(self.old_network, 'P-1')
        pipe_new = get_pipe(self.new_network, 'P-1')
        pipe_old.diameter = 100
        self.assertFalse(pipe_old.diameter == pipe_new.diameter)

    def test_pump(self):
        self.compare_pumps(self.old_network, self.new_network)
        pump_old = get_pump(self.old_network, 'PU-1')
        pump_new = get_pump(self.new_network, 'PU-1')
        pump_old.power = 100
        self.assertFalse(pump_old.power == pump_new.power)

    def test_valve(self):
        self.compare_valves(self.old_network, self.new_network)
        valve_old = get_valve(self.old_network, 'V-1')
        valve_new = get_valve(self.new_network, 'V-1')
        valve_old.diameter = 1
        self.assertFalse(valve_old.diameter == valve_new.diameter)

    def test_options(self):
        self.compare_options(self.old_network, self.new_network)
        old_options = self.old_network.options
        new_options = self.new_network.options
        old_options.demandmodel = 'PDA'
        self.assertFalse(old_options == new_options)

    def test_times(self):
        self.compare_times(self.old_network, self.new_network)
        old_times = self.old_network.times
        new_times = self.new_network.times
        old_times.duration = datetime.timedelta(hours=2)
        self.assertFalse(old_times == new_times)

    def test_report_parameter(self):
        self.compare_reportparameters(self.old_network, self.new_network)
        old_parameter = self.old_network.reportparameter
        new_parameter = self.new_network.reportparameter
        old_parameter.demand = 'NO'
        self.assertFalse(old_parameter == new_parameter)

    def test_report_precision(self):
        self.compare_reportprecision(self.old_network, self.new_network)
        old_precision = self.old_network.reportprecision
        new_precision = self.new_network.reportprecision
        old_precision.demand = 4
        self.assertFalse(old_precision == new_precision)

    def test_report(self):
        self.compare_report(self.old_network, self.new_network)
        old_report = self.old_network.report
        new_report = self.new_network.report
        old_report.status = 'YES'
        self.assertFalse(old_report == new_report)


class PatternCurveDeepcopyTest(DeepcopyTest):
    def setUp(self) -> None:
        self.model = PatternCurveModel()
        self.old_network = self.model.network
        self.new_network = deepcopy(self.model.network)

    def test_curve(self):
        self.compare_curves(self.old_network, self.new_network)

    def test_patterns(self):
        self.compare_patterns(self.old_network, self.new_network)
        

if __name__ == '__main__':
    unittest.main()

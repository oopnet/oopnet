import unittest
import datetime

from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve
from oopnet.elements.system_operation import Curve
from oopnet.utils.getters.get_by_id import get_curve, get_pattern, get_link
from oopnet.utils.getters.element_lists import get_patterns


class PoulakisEnhancedReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import PoulakisEnhancedPDAModel
        self.model = PoulakisEnhancedPDAModel()

    def test_junctions(self):
        self.assertEqual(self.model.n_junctions, len(self.model.network._nodes['junctions']))
        for j in self.model.network._nodes['junctions'].values():
            self.assertIsInstance(j, Junction)
            self.assertEqual(50, j.demand)
            self.assertTrue('J' in j.id)

    def test_tanks(self):
        self.assertEqual(self.model.n_tanks, len(self.model.network._nodes['tanks']))
        for t in self.model.network._nodes['tanks'].values():
            self.assertIsInstance(t, Tank)
            self.assertEqual(50, t.diam)
            self.assertTrue('J' in t.id)

    def test_reservoirs(self):
        self.assertEqual(self.model.n_reservoirs, len(self.model.network._nodes['reservoirs']))
        for r in self.model.network._nodes['reservoirs'].values():
            self.assertIsInstance(r, Reservoir)
            self.assertEqual(52, r.head)
            self.assertTrue('J' in r.id)

    def test_pipes(self):
        self.assertEqual(self.model.n_pipes, len(self.model.network._links['pipes']))
        for p in self.model.network._links['pipes'].values():
            self.assertIsInstance(p, Pipe)
            self.assertEqual(0.26, p.roughness)
            self.assertTrue(p.diameter in [600, 450, 300])
            self.assertTrue('P' in p.id)

    def test_pumps(self):
        self.assertEqual(self.model.n_pumps, len(self.model.network._links['pumps']))
        for p in self.model.network._links['pumps'].values():
            self.assertIsInstance(p, Pump)
            self.assertIsInstance(p.head, Curve)
            self.assertTrue('P' in p.id)

    def test_valves(self):
        self.assertEqual(self.model.n_valves, len(self.model.network._links['valves']))
        for v in self.model.network._links['valves'].values():
            self.assertIsInstance(v, Valve)
            self.assertEqual(500, v.diameter)
            self.assertTrue('P' in v.id)

    def test_curves(self):
        c1 = get_curve(self.model.network, '1')
        self.assertEqual([50, 100], c1.xvalues)
        self.assertEqual([5, 10], c1.yvalues)

        c2 = get_curve(self.model.network, '2')
        self.assertEqual([50], c2.xvalues)
        self.assertEqual([50], c2.yvalues)

        c3 = get_curve(self.model.network, '3')
        self.assertEqual([2, 5], c3.xvalues)
        self.assertEqual([20, 50], c3.yvalues)

    def test_options(self):
        options = self.model.network.options
        self.assertEqual('LPS', options.units)
        self.assertEqual(40, options.trials)
        self.assertEqual('D-W', options.headloss)
        self.assertEqual(1.00000004749745E-10, options.accuracy)
        self.assertEqual(1, options.demandmultiplier)
        self.assertEqual(1, options.emitterexponent)
        self.assertEqual(1, options.pattern)
        self.assertEqual('PDA', options.demandmodel)
        self.assertEqual(0, options.minimumpressure)
        self.assertEqual(10, options.requiredpressure)
        self.assertEqual(0.5, options.pressureexponent)
        self.assertEqual(('CONTINUE', 10), options.unbalanced)
        self.assertEqual(1, options.viscosity)
        self.assertEqual(1.00000004749745E-10, options.tolerance)

    def test_report(self):
        report = self.model.network.report
        self.assertEqual('FULL', report.status)
        self.assertEqual('NO', report.summary)

    def test_times(self):
        times = self.model.network.times
        self.assertEqual(datetime.timedelta(hours=0), times.duration)
        self.assertEqual(datetime.timedelta(hours=1), times.hydraulictimestep)
        self.assertEqual(datetime.timedelta(minutes=5), times.qualitytimestep)
        self.assertEqual(datetime.timedelta(hours=1), times.patterntimestep)
        self.assertEqual(datetime.timedelta(), times.patternstart)
        self.assertEqual(datetime.timedelta(hours=1), times.reporttimestep)
        self.assertEqual(datetime.timedelta(), times.reportstart)
        self.assertEqual(datetime.timedelta(), times.startclocktime)
        self.assertEqual('NONE', times.statistic)

    def test_run(self):
        rpt = self.model.network.run()

    # todo: add options, reportparameter, curve, pattern ... tests


class MicropolisReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import MicropolisModel
        self.model = MicropolisModel()

    def test_controls(self):
        self.assertEqual(self.model.n_controls, len(self.model.network.controls))

    def test_rules(self):
        self.assertEqual(self.model.n_rules, len(self.model.network._rules))

    def test_patterns(self):
        self.assertEqual(self.model.n_patterns, len(self.model.network._patterns))
        for pat in get_patterns(self.model.network):
            self.assertEqual(24, len(pat.multipliers))

        p = get_pattern(self.model.network, '3')
        self.assertEqual([0.96, 0.96, 0.96, 0.96, 1.06, 1.07, 1.06, 0.96, 0.96, 0.96, 0.96, 0.96, 1.065, 1.075, 1.056,
                          0.96, 0.96, 0.96, 0.96, 0.96, 1.065, 1.075, 1.065, 0.96], p.multipliers)

    def test_run(self):
        rpt = self.model.network.run()

    def test_options(self):
        options = self.model.network.options
        self.assertEqual('LPS', options.units)
        self.assertEqual(40, options.trials)
        self.assertEqual('D-W', options.headloss)
        self.assertEqual(0.001, options.accuracy)
        self.assertEqual(1, options.demandmultiplier)
        self.assertEqual(0.5, options.emitterexponent)
        defpat = get_pattern(self.model.network, 'DefPat')
        self.assertEqual(defpat, options.pattern)
        self.assertEqual('DDA', options.demandmodel)
        self.assertEqual(0.0, options.minimumpressure)
        self.assertEqual(0.1, options.requiredpressure)
        self.assertEqual(0.5, options.pressureexponent)
        self.assertEqual(('CONTINUE', 10), options.unbalanced)
        self.assertEqual(1, options.viscosity)
        self.assertEqual(0.01, options.tolerance)

    def test_report(self):
        report = self.model.network.report
        self.assertEqual('NO', report.status)
        self.assertEqual('NO', report.summary)

    def test_times(self):
        times = self.model.network.times
        self.assertEqual(datetime.timedelta(hours=240), times.duration)
        self.assertEqual(datetime.timedelta(hours=1), times.hydraulictimestep)
        self.assertEqual(datetime.timedelta(minutes=5), times.qualitytimestep)
        self.assertEqual(datetime.timedelta(hours=1), times.patterntimestep)
        self.assertEqual(datetime.timedelta(), times.patternstart)
        self.assertEqual(datetime.timedelta(hours=1), times.reporttimestep)
        self.assertEqual(datetime.timedelta(), times.reportstart)
        self.assertEqual(datetime.timedelta(), times.startclocktime)
        self.assertEqual('NONE', times.statistic)


class RulesModelReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import RulesModel
        self.model = RulesModel()

    def test_options(self):
        options = self.model.network.options
        self.assertEqual('LPS', options.units)
        self.assertEqual(40, options.trials)
        self.assertEqual('H-W', options.headloss)
        self.assertEqual(0.001, options.accuracy)
        self.assertEqual(1, options.demandmultiplier)
        self.assertEqual(0.5, options.emitterexponent)
        self.assertEqual(1, options.pattern)
        self.assertEqual('DDA', options.demandmodel)
        self.assertEqual(0.0, options.minimumpressure)
        self.assertEqual(0.1, options.requiredpressure)
        self.assertEqual(0.5, options.pressureexponent)
        self.assertEqual(('CONTINUE', 10), options.unbalanced)
        self.assertEqual(1, options.viscosity)
        self.assertEqual(0.01, options.tolerance)

    def test_run(self):
        rpt = self.model.network.run()

    def test_rules(self):
        self.assertEqual(self.model.n_rules, len(self.model.network._rules))


class CTownReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import CTownModel
        self.model = CTownModel()

    def test_run(self):
        rpt = self.model.network.run()


class ETownReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        from testing.base import ETownModel
        self.model = ETownModel()

    def test_vertices(self):
        l = get_link(self.model.network, '3569')
        self.assertEqual(3, len(l.vertices))


if __name__ == '__main__':
    unittest.main()

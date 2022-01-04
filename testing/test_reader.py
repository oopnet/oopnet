import unittest

from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve
from oopnet.api import Run

from testing.base import PoulakisEnhancedPDAModel, MicropolisModel


class PoulakisEnhancedReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_junctions(self):
        self.assertEqual(self.model.n_junctions, len(self.model.network.junctions))
        for j in self.model.network.junctions.values():
            self.assertIsInstance(j, Junction)
            self.assertEqual(50, j.demand)
            self.assertTrue('J' in j.id)

    def test_tanks(self):
        self.assertEqual(self.model.n_tanks, len(self.model.network.tanks))
        for t in self.model.network.tanks.values():
            self.assertIsInstance(t, Tank)
            self.assertEqual(50, t.diam)
            self.assertTrue('J' in t.id)

    def test_reservoirs(self):
        self.assertEqual(self.model.n_reservoirs, len(self.model.network.reservoirs))
        for r in self.model.network.reservoirs.values():
            self.assertIsInstance(r, Reservoir)
            self.assertEqual(52, r.head)
            self.assertTrue('J' in r.id)

    def test_pipes(self):
        self.assertEqual(self.model.n_pipes, len(self.model.network.pipes))
        for p in self.model.network.pipes.values():
            self.assertIsInstance(p, Pipe)
            self.assertEqual(0.26, p.roughness)
            self.assertTrue(p.diameter in [600, 450, 300])
            self.assertTrue('P' in p.id)

    def test_pumps(self):
        self.assertEqual(self.model.n_pumps, len(self.model.network.pumps))
        for p in self.model.network.pumps.values():
            self.assertIsInstance(p, Pump)
            self.assertEqual('HEAD', p.keyword)
            self.assertTrue('P' in p.id)

    def test_valves(self):
        self.assertEqual(self.model.n_valves, len(self.model.network.valves))
        for v in self.model.network.valves.values():
            self.assertIsInstance(v, Valve)
            self.assertEqual(500, v.diameter)
            self.assertTrue('P' in v.id)

    # todo: add options, reportparameter, curve, pattern ... tests


class MicorpolisReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = MicropolisModel()

    def test_controls(self):
        self.assertEqual(self.model.n_controls, len(self.model.network.controls))

    def test_patterns(self):
        self.assertEqual(self.model.n_patterns, len(self.model.network.patterns))

    def test_curves(self):
        self.assertEqual(self.model.n_curves, len(self.model.network.curves))

    def test_run(self):
        Run(self.model.network)


if __name__ == '__main__':
    unittest.main()

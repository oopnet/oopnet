import unittest

from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve

from testing.base import PoulakisEnhancedPDAModel


class PoulakisEnhancedReaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_junctions(self):
        self.assertEqual(self.model.n_junctions, len(self.model.network.junctions))
        for index, j in enumerate(self.model.network.junctions):
            self.assertIsInstance(j, Junction)
            self.assertEqual(50, j.demand)
            self.assertTrue('J' in j.id)

    def test_tanks(self):
        self.assertEqual(self.model.n_tanks, len(self.model.network.tanks))
        for index, t in enumerate(self.model.network.tanks):
            self.assertIsInstance(t, Tank)
            self.assertEqual(50, t.diam)
            self.assertTrue('J' in t.id)

    def test_reservoirs(self):
        self.assertEqual(self.model.n_reservoirs, len(self.model.network.reservoirs))
        for index, r in enumerate(self.model.network.reservoirs):
            self.assertIsInstance(r, Reservoir)
            self.assertEqual(52, r.head)
            self.assertTrue('J' in r.id)

    def test_pipes(self):
        self.assertEqual(self.model.n_pipes, len(self.model.network.pipes))
        for index, p in enumerate(self.model.network.pipes):
            self.assertIsInstance(p, Pipe)
            self.assertEqual(0.26, p.roughness)
            self.assertTrue(p.diameter in [600, 450, 300])
            self.assertTrue('P' in p.id)

    def test_pumps(self):
        self.assertEqual(self.model.n_pumps, len(self.model.network.pumps))
        for index, p in enumerate(self.model.network.pumps):
            self.assertIsInstance(p, Pump)
            self.assertEqual('HEAD', p.keyword)
            self.assertTrue('P' in p.id)

    def test_valves(self):
        self.assertEqual(self.model.n_valves, len(self.model.network.valves))
        for index, v in enumerate(self.model.network.valves):
            self.assertIsInstance(v, Valve)
            self.assertEqual(500, v.diameter)
            self.assertTrue('P' in v.id)

    # todo: add options, reportparameter, curve, pattern ... tests

if __name__ == '__main__':
    unittest.main()

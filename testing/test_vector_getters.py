import unittest

import numpy as np

from oopnet.utils.getters.vectors import v_length, v_diameter, v_roughness, v_minorloss, v_elevation, \
    v_emittercoefficient, v_demand, v_head, v_initlevel, v_minlevel, v_maxlevel, v_tankdiameter, v_minvolume

from testing.base import SimpleModel


class SimplePropertyGetterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_v_length(self):
        length = v_length(self.model.network)
        self.assertIsInstance(length, np.ndarray)
        self.assertEqual(self.model.n_pipes, len(length))

    def test_v_diameter(self):
        diameter = v_diameter(self.model.network)
        self.assertIsInstance(diameter, np.ndarray)
        self.assertEqual(self.model.n_pipes + self.model.n_valves, len(diameter))

    def test_v_roughness(self):
        roughness = v_roughness(self.model.network)
        self.assertIsInstance(roughness, np.ndarray)
        self.assertEqual(self.model.n_pipes, len(roughness))

    def test_v_minorloss(self):
        minorloss = v_minorloss(self.model.network)
        self.assertIsInstance(minorloss, np.ndarray)
        self.assertEqual(self.model.n_pipes, len(minorloss))

    def test_v_elevation(self):
        elevation = v_elevation(self.model.network)
        self.assertIsInstance(elevation, np.ndarray)
        self.assertEqual(self.model.n_nodes, len(elevation))

    def test_v_emittercoefficient(self):
        emittercoefficient = v_emittercoefficient(self.model.network)
        self.assertIsInstance(emittercoefficient, np.ndarray)
        self.assertEqual(self.model.n_junctions, len(emittercoefficient))

    def test_v_demand(self):
        demand = v_demand(self.model.network)
        self.assertIsInstance(demand, np.ndarray)
        self.assertEqual(self.model.n_junctions, len(demand))

    def test_v_head(self):
        head = v_head(self.model.network)
        self.assertIsInstance(head, np.ndarray)
        self.assertEqual(self.model.n_reservoirs, len(head))

    def test_v_initlevel(self):
        initlevel = v_initlevel(self.model.network)
        self.assertIsInstance(initlevel, np.ndarray)
        self.assertEqual(self.model.n_tanks, len(initlevel))

    def test_v_minlevel(self):
        minlevel = v_minlevel(self.model.network)
        self.assertIsInstance(minlevel, np.ndarray)
        self.assertEqual(self.model.n_tanks, len(minlevel))

    def test_v_maxlevel(self):
        maxlevel = v_maxlevel(self.model.network)
        self.assertIsInstance(maxlevel, np.ndarray)
        self.assertEqual(self.model.n_tanks, len(maxlevel))

    def test_v_tankdiameter(self):
        tankdiameter = v_tankdiameter(self.model.network)
        self.assertIsInstance(tankdiameter, np.ndarray)
        self.assertEqual(self.model.n_tanks, len(tankdiameter))

    def test_v_minvolume(self):
        initlevel = v_minvolume(self.model.network)
        self.assertIsInstance(initlevel, np.ndarray)
        self.assertEqual(self.model.n_tanks, len(initlevel))

if __name__ == '__main__':
    unittest.main()

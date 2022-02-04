import unittest

from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve, Node, Link
from oopnet.utils.getters import *

from testing.base import PoulakisEnhancedPDAModel


class PoulakisEnhancedPDAModelTopologyGetterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_get_neighbor_links(self):
        neighs = get_neighbor_links(self.model.network, get_link(self.model.network, 'P-45'))
        self.assertEqual(3, len(neighs))
        for l in neighs:
            self.assertIsInstance(l, Link)
        for lid in ['P-34', 'P-39', 'P-50']:
            self.assertTrue(get_link(self.model.network, lid) in neighs)

    def test_get_next_neighbor_links(self):
        neighs = get_next_neighbor_links(self.model.network, get_link(self.model.network, 'P-51'))
        print(neighs)
        self.assertEqual(4, len(neighs))
        for l in neighs:
            self.assertIsInstance(l, Link)
        for lid in ['P-29', 'P-35', 'P-41', 'P-47']:
            self.assertTrue(get_link(self.model.network, lid) in neighs)

    def test_get_neighbor_nodes(self):
        neighs = get_neighbor_nodes(self.model.network, get_node(self.model.network, 'J-31'))
        self.assertEqual(2, len(neighs))
        for n in neighs:
            self.assertIsInstance(n, Node)
        for nid in ['J-25', 'J-30']:
            self.assertTrue(get_node(self.model.network, nid) in neighs)

    def test_get_next_neighbor_nodes(self):
        neighs = get_next_neighbor_nodes(self.model.network, get_node(self.model.network, 'J-31'))
        self.assertEqual(3, len(neighs))
        for n in neighs:
            self.assertIsInstance(n, Node)
        for nid in ['J-19', 'J-24', 'J-29']:
            self.assertTrue(get_node(self.model.network, nid) in neighs)

    def test_get_inflow_neighbor_nodes(self):
        j = get_junction(self.model.network, 'J-07')
        j.demand = -1
        neighs = get_inflow_neighbor_nodes(self.model.network)
        self.assertEqual(4, len(neighs))
        for n in neighs:
            self.assertIsInstance(n, Node)
        for nid in ['J-02', 'J-26', 'J-06', 'J-13']:
            self.assertTrue(get_node(self.model.network, nid) in neighs)

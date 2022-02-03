import unittest

import networkx as nx

from oopnet.graph.graph import Graph, DiGraph, MultiGraph, MultiDiGraph
from oopnet.elements.network_components import Pipe
from oopnet.utils.getters.get_by_id import get_link
from testing.base import PoulakisEnhancedPDAModel


class PoulakisEnhancedGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_graph(self):
        g = Graph(self.model.network)
        self.assertIsInstance(g, nx.Graph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links - 1, len(g.edges))  # Graph not able to have two links between two edges

    def test_digraph(self):
        g = DiGraph(self.model.network)
        self.assertIsInstance(g, nx.DiGraph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links, len(g.edges))

    def test_multigraph(self):
        g = MultiGraph(self.model.network)
        self.assertIsInstance(g, nx.MultiGraph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links, len(g.edges))

    def test_multidigraph(self):
        g = MultiDiGraph(self.model.network)
        self.assertIsInstance(g, nx.MultiDiGraph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links, len(g.edges))

    def test_report_weight(self):
        self.model.network.reportparameter.headloss = 'YES'
        self.model.network.reportparameter.length = 'YES'
        rpt = self.model.network.run()
        headloss = rpt.headloss
        g = MultiGraph(self.model.network, weight=headloss, default=0)
        self.assertIsInstance(g, nx.Graph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links, len(g.edges))

        weights = nx.get_edge_attributes(g, 'weight')
        for link_id, link_hl in headloss.iteritems():
            l = get_link(self.model.network, link_id)
            try:
                link_weight = weights[(l.endnode.id, l.startnode.id, 0)]
            except KeyError:
                link_weight = weights[(l.startnode.id, l.endnode.id, 0)]
            if isinstance(l, Pipe):
                self.assertEqual(link_hl, link_weight)
            else:
                self.assertEqual(link_hl, 0)


if __name__ == '__main__':
    unittest.main()

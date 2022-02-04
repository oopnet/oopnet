import unittest

import networkx as nx

from oopnet.graph.graph import Graph, DiGraph, MultiGraph, MultiDiGraph, onlinks2nxlinks, nxlinks2onlinks, \
    nxedge2onlink_id, edgeresult2pandas
from oopnet.elements.network_components import Pipe
from oopnet.utils.getters.get_by_id import get_link
from testing.base import ETownModel, CTownModel, PoulakisEnhancedPDAModel


class CTownModelGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = CTownModel()

    def test_graph(self):
        g = Graph(self.model.network)
        self.assertIsInstance(g, nx.Graph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links, len(g.edges))  # Graph not able to have two links between two edges

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

    def test_edgeresult2pandas_multigraph(self):
        g = MultiGraph(self.model.network)
        data = nx.edge_betweenness_centrality(g)
        edgeresult2pandas(g, data)

    def test_edgeresult2pandas_graph(self):
        g = Graph(self.model.network)
        data = nx.edge_betweenness_centrality(g)
        edgeresult2pandas(g, data)


class PoulakisEnhancedPDAGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_edgeresult2pandas_multigraph(self):
        g = MultiGraph(self.model.network)
        data = nx.edge_betweenness_centrality(g)
        edgeresult2pandas(g, data)

    def test_edgeresult2pandas_graph(self):
        g = Graph(self.model.network)
        data = nx.edge_betweenness_centrality(g)
        edgeresult2pandas(g, data)


class ETownModelGraphTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = ETownModel()

    def test_graph(self):
        g = Graph(self.model.network)
        self.assertIsInstance(g, nx.Graph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links - 21, len(g.edges))  # Graph not able to have two links between two edges

    def test_digraph(self):
        g = DiGraph(self.model.network)
        self.assertIsInstance(g, nx.DiGraph)
        self.assertEqual(self.model.n_nodes, len(g.nodes))
        self.assertEqual(self.model.n_links - 8, len(g.edges))

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

    def test_onlinks2nxlinks(self):
        nxlinks = onlinks2nxlinks(self.model.network)
        self.assertEqual(self.model.n_links, len(nxlinks))
        for sid, eid in nxlinks:
            self.assertIsInstance(sid, str)
            self.assertIsInstance(eid, str)

    def test_nxlinks2onlinks_multigraph(self):
        g = MultiGraph(self.model.network)
        onlinks = nxlinks2onlinks(g)
        for lid in onlinks:
            l = get_link(self.model.network, lid)

    def test_nxlinks2onlinks_graph(self):
        g = Graph(self.model.network)
        onlinks = nxlinks2onlinks(g)
        for lid in onlinks:
            l = get_link(self.model.network, lid)

    def test_nxedge2onlinkid_multigraph(self):
        g = MultiGraph(self.model.network)
        for edge in [('40144', '40143'), ('40170', '40169')]:
            lids = nxedge2onlink_id(g, edge)
            for lid in lids:
                get_link(self.model.network, lid)

    def test_nxedge2onlinkid_graph(self):
        g = Graph(self.model.network)
        for edge in [('40144', '40143'), ('40170', '40169')]:
            lids = nxedge2onlink_id(g, edge)
            for lid in lids:
                get_link(self.model.network, lid)


if __name__ == '__main__':
    unittest.main()

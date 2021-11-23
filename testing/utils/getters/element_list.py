import unittest
from testing.base_cases import PoulakisEnhancedPDAModel
from oopnet.elements.network_components import *
from oopnet.utils.getters.element_lists import *


class PoulakisEnhancedPDAListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    def test_get_junction_ids(self):
        jids = get_junction_ids(self.model.network)
        self.assertEqual(self.model.n_junctions, len(jids))
        self.assertEqual(self.model.n_junctions, len(set(jids)))
        self.assertIsInstance(jids, list)
        
        for jid in jids:
            self.assertIsInstance(jid, str)
            j = self.model.network.networkhash['node'][jid]
            self.assertIsInstance(j, Junction)
            
    def test_get_tank_ids(self):
        tids = get_tank_ids(self.model.network)
        self.assertEqual(self.model.n_tanks, len(tids))
        self.assertEqual(self.model.n_tanks, len(set(tids)))
        self.assertIsInstance(tids, list)

        for tid in tids:
            self.assertIsInstance(tid, str)
            t = self.model.network.networkhash['node'][tid]
            self.assertIsInstance(t, Tank)
            
    def test_get_reservoirs_ids(self):
        rids = get_reservoir_ids(self.model.network)
        self.assertEqual(self.model.n_reservoirs, len(rids))
        self.assertEqual(self.model.n_reservoirs, len(set(rids)))
        self.assertIsInstance(rids, list)

        for rid in rids:
            self.assertIsInstance(rid, str)
            r = self.model.network.networkhash['node'][rid]
            self.assertIsInstance(r, Reservoir)

    def test_get_node_ids(self):
        nids = get_node_ids(self.model.network)
        self.assertEqual(self.model.n_nodes, len(nids))
        self.assertEqual(self.model.n_nodes, len(set(nids)))
        self.assertIsInstance(nids, list)

        for nid in nids:
            self.assertIsInstance(nid, str)
            n = self.model.network.networkhash['node'][nid]
            self.assertIsInstance(n, Node)

    def test_get_pipe_ids(self):
        pids = get_pipe_ids(self.model.network)
        self.assertEqual(self.model.n_pipes, len(pids))
        self.assertEqual(self.model.n_pipes, len(set(pids)))
        self.assertIsInstance(pids, list)

        for pid in pids:
            self.assertIsInstance(pid, str)
            p = self.model.network.networkhash['link'][pid]
            self.assertIsInstance(p, Pipe)

    def test_get_pump_ids(self):
        pids = get_pump_ids(self.model.network)
        self.assertEqual(self.model.n_pumps, len(pids))
        self.assertEqual(self.model.n_pumps, len(set(pids)))
        self.assertIsInstance(pids, list)

        for pid in pids:
            self.assertIsInstance(pid, str)
            p = self.model.network.networkhash['link'][pid]
            self.assertIsInstance(p, Pump)
            
    def test_get_valve_ids(self):
        vids = get_valve_ids(self.model.network)
        self.assertEqual(self.model.n_valves, len(vids))
        self.assertEqual(self.model.n_valves, len(set(vids)))
        self.assertIsInstance(vids, list)

        for vid in vids:
            self.assertIsInstance(vid, str)
            v = self.model.network.networkhash['link'][vid]
            self.assertIsInstance(v, Valve)
            
    def test_get_link_ids(self):
        lids = get_link_ids(self.model.network)
        self.assertEqual(self.model.n_links, len(lids))
        self.assertEqual(self.model.n_links, len(set(lids)))
        self.assertIsInstance(lids, list)

        for lid in lids:
            self.assertIsInstance(lid, str)
            l = self.model.network.networkhash['link'][lid]
            self.assertIsInstance(l, Link)

    def test_get_junctions(self):
        junctions = get_junctions(self.model.network)
        self.assertEqual(self.model.n_junctions, len(junctions))
        self.assertEqual(self.model.n_junctions, len(set(junctions)))
        self.assertIsInstance(junctions, list)

        for junction in junctions:
            self.assertIsInstance(junction, Junction)

    def test_get_tanks(self):
        tanks = get_tanks(self.model.network)
        self.assertEqual(self.model.n_tanks, len(tanks))
        self.assertEqual(self.model.n_tanks, len(set(tanks)))
        self.assertIsInstance(tanks, list)

        for tank in tanks:
            self.assertIsInstance(tank, Tank)

    def test_get_reservoirs(self):
        reservoirs = get_reservoirs(self.model.network)
        self.assertEqual(self.model.n_reservoirs, len(reservoirs))
        self.assertEqual(self.model.n_reservoirs, len(set(reservoirs)))
        self.assertIsInstance(reservoirs, list)

        for reservoir in reservoirs:
            self.assertIsInstance(reservoir, Reservoir)

    def test_get_nodes(self):
        nodes = get_nodes(self.model.network)
        self.assertEqual(self.model.n_nodes, len(nodes))
        self.assertEqual(self.model.n_nodes, len(set(nodes)))
        self.assertIsInstance(nodes, list)

        for node in nodes:
            self.assertIsInstance(node, Node)

    def test_get_pipes(self):
        pipes = get_pipes(self.model.network)
        self.assertEqual(self.model.n_pipes, len(pipes))
        self.assertEqual(self.model.n_pipes, len(set(pipes)))
        self.assertIsInstance(pipes, list)

        for pipe in pipes:
            self.assertIsInstance(pipe, Pipe)

    def test_get_pumps(self):
        pumps = get_pumps(self.model.network)
        self.assertEqual(self.model.n_pumps, len(pumps))
        self.assertEqual(self.model.n_pumps, len(set(pumps)))
        self.assertIsInstance(pumps, list)

        for pump in pumps:
            self.assertIsInstance(pump, Pump)

    def test_get_valves(self):
        valves = get_valves(self.model.network)
        self.assertEqual(self.model.n_valves, len(valves))
        self.assertEqual(self.model.n_valves, len(set(valves)))
        self.assertIsInstance(valves, list)

        for valve in valves:
            self.assertIsInstance(valve, Valve)

    def test_get_links(self):
        links = get_links(self.model.network)
        self.assertEqual(self.model.n_links, len(links))
        self.assertEqual(self.model.n_links, len(set(links)))
        self.assertIsInstance(links, list)

        for link in links:
            self.assertIsInstance(link, Link)


if __name__ == '__main__':
    unittest.main()

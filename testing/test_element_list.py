import unittest

from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve, Node, Link
from oopnet.utils.getters import *

from testing.base import SimpleModel


class SimpleListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_get_junction_ids(self):
        jids = get_junction_ids(self.model.network)
        self.assertEqual(self.model.n_junctions, len(jids))
        self.assertEqual(self.model.n_junctions, len(set(jids)))
        self.assertIsInstance(jids, list)
        
        for jid in jids:
            self.assertIsInstance(jid, str)
            j = get_node(self.model.network, jid)
            self.assertIsInstance(j, Junction)
            
    def test_get_tank_ids(self):
        tids = get_tank_ids(self.model.network)
        self.assertEqual(self.model.n_tanks, len(tids))
        self.assertEqual(self.model.n_tanks, len(set(tids)))
        self.assertIsInstance(tids, list)

        for tid in tids:
            self.assertIsInstance(tid, str)
            t = get_node(self.model.network, tid)
            self.assertIsInstance(t, Tank)
            
    def test_get_reservoirs_ids(self):
        rids = get_reservoir_ids(self.model.network)
        self.assertEqual(self.model.n_reservoirs, len(rids))
        self.assertEqual(self.model.n_reservoirs, len(set(rids)))
        self.assertIsInstance(rids, list)

        for rid in rids:
            self.assertIsInstance(rid, str)
            r = get_node(self.model.network, rid)
            self.assertIsInstance(r, Reservoir)

    def test_get_node_ids(self):
        nids = get_node_ids(self.model.network)
        self.assertEqual(self.model.n_nodes, len(nids))
        self.assertEqual(self.model.n_nodes, len(set(nids)))
        self.assertIsInstance(nids, list)

        for nid in nids:
            self.assertIsInstance(nid, str)
            n = get_node(self.model.network, nid)
            self.assertIsInstance(n, Node)

    def test_get_pipe_ids(self):
        pids = get_pipe_ids(self.model.network)
        self.assertEqual(self.model.n_pipes, len(pids))
        self.assertEqual(self.model.n_pipes, len(set(pids)))
        self.assertIsInstance(pids, list)

        for pid in pids:
            self.assertIsInstance(pid, str)
            p = get_link(self.model.network, pid)
            self.assertIsInstance(p, Pipe)

    def test_get_pump_ids(self):
        pids = get_pump_ids(self.model.network)
        self.assertEqual(self.model.n_pumps, len(pids))
        self.assertEqual(self.model.n_pumps, len(set(pids)))
        self.assertIsInstance(pids, list)

        for pid in pids:
            self.assertIsInstance(pid, str)
            p = get_link(self.model.network, pid)
            self.assertIsInstance(p, Pump)
            
    def test_get_valve_ids(self):
        vids = get_valve_ids(self.model.network)
        self.assertEqual(self.model.n_valves, len(vids))
        self.assertEqual(self.model.n_valves, len(set(vids)))
        self.assertIsInstance(vids, list)

        for vid in vids:
            self.assertIsInstance(vid, str)
            v = get_link(self.model.network, vid)
            self.assertIsInstance(v, Valve)
            
    def test_get_link_ids(self):
        lids = get_link_ids(self.model.network)
        self.assertEqual(self.model.n_links, len(lids))
        self.assertIsInstance(lids, list)

        for lid in lids:
            self.assertIsInstance(lid, str)
            l = get_link(self.model.network, lid)
            self.assertIsInstance(l, Link)

    def test_get_junctions(self):
        junctions = get_junctions(self.model.network)
        self.assertEqual(self.model.n_junctions, len(junctions))
        self.assertIsInstance(list(junctions), list)

        for junction in junctions:
            self.assertIsInstance(junction, Junction)

    def test_get_tanks(self):
        tanks = get_tanks(self.model.network)
        self.assertEqual(self.model.n_tanks, len(tanks))
        self.assertIsInstance(list(tanks), list)

        for tank in tanks:
            self.assertIsInstance(tank, Tank)

    def test_get_reservoirs(self):
        reservoirs = get_reservoirs(self.model.network)
        self.assertEqual(self.model.n_reservoirs, len(reservoirs))
        self.assertIsInstance(list(reservoirs), list)

        for reservoir in reservoirs:
            self.assertIsInstance(reservoir, Reservoir)

    def test_get_nodes(self):
        nodes = get_nodes(self.model.network)
        self.assertEqual(self.model.n_nodes, len(nodes))
        self.assertIsInstance(list(nodes), list)

        for node in nodes:
            self.assertIsInstance(node, Node)

    def test_get_pipes(self):
        pipes = get_pipes(self.model.network)
        self.assertEqual(self.model.n_pipes, len(pipes))
        self.assertIsInstance(list(pipes), list)

        for pipe in pipes:
            self.assertIsInstance(pipe, Pipe)

    def test_get_pumps(self):
        pumps = get_pumps(self.model.network)
        self.assertEqual(self.model.n_pumps, len(pumps))
        self.assertIsInstance(list(pumps), list)

        for pump in pumps:
            self.assertIsInstance(pump, Pump)

    def test_get_valves(self):
        valves = get_valves(self.model.network)
        self.assertEqual(self.model.n_valves, len(valves))
        self.assertIsInstance(list(valves), list)

        for valve in valves:
            self.assertIsInstance(valve, Valve)

    def test_get_links(self):
        links = get_links(self.model.network)
        self.assertEqual(self.model.n_links, len(links))
        self.assertIsInstance(list(links), list)

        for link in links:
            self.assertIsInstance(link, Link)


if __name__ == '__main__':
    unittest.main()

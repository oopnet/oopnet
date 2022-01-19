import unittest

from oopnet.elements import Curve, Junction, Tank, Reservoir, Pipe, Pump, Valve, Node, Link
from oopnet.utils.getters import *

from testing.base import SimpleModel


class SimpleElementGetterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_get_junction(self):
        for jid, junction in self.model.network._junctions.items():
            j = get_junction(self.model.network, jid)
            self.assertIsInstance(j, Junction)
            self.assertEqual(junction, j)

    def test_get_tank(self):
        for tid, tank in self.model.network._tanks.items():
            t = get_tank(self.model.network, tid)
            self.assertIsInstance(t, Tank)
            self.assertEqual(tank, t)
            
    def test_get_reservoir(self):
        for rid, reservoir in self.model.network._reservoirs.items():
            r = get_reservoir(self.model.network, rid)
            self.assertIsInstance(r, Reservoir)
            self.assertEqual(reservoir, r)
            
    def test_get_node(self):
        for nid, node in self.model.network._nodes.items():
            n = get_node(self.model.network, nid)
            self.assertIsInstance(n, Node)
            self.assertEqual(node, n)

    def test_get_pipe(self):
        for pid, pipe in self.model.network._pipes.items():
            p = get_pipe(self.model.network, pid)
            self.assertIsInstance(p, Pipe)
            self.assertEqual(pipe, p)
            
    def test_get_pump(self):
        for pid, pump in self.model.network._pumps.items():
            p = get_pump(self.model.network, pid)
            self.assertIsInstance(p, Pump)
            self.assertEqual(pump, p)
            
    def test_get_valve(self):
        for vid, valve in self.model.network._valves.items():
            v = get_valve(self.model.network, vid)
            self.assertIsInstance(v, Valve)
            self.assertEqual(valve, v)
            
    def test_get_link(self):
        for lid, link in self.model.network._links.items():
            l = get_link(self.model.network, lid)
            self.assertIsInstance(l, Link)
            self.assertEqual(link, l)

    def test_get_curve(self):
        for cid, curve in self.model.network._curves.items():
            c = get_curve(self.model.network, cid)
            self.assertIsInstance(c, Curve)
            self.assertEqual(curve, c)

    # todo: implement
    def test_get_pattern(self):
        pass

    def test_get_rule(self):
        pass


if __name__ == '__main__':
    unittest.main()

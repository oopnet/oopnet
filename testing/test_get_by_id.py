import unittest

from oopnet.elements.system_operation import Curve
from oopnet.utils.getters import *
from oopnet.elements.network_components import Junction, Tank, Reservoir, Pipe, Pump, Valve, Node, Link

from testing.base import SimpleModel


class SimpleElementGetterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_get_junction(self):
        for junction in self.model.network.junctions:
            jid = junction.id
            j = get_junction(self.model.network, jid)
            self.assertIsInstance(j, Junction)
            self.assertEqual(junction, j)

    def test_get_tank(self):
        for tank in self.model.network.tanks:
            tid = tank.id
            t = get_tank(self.model.network, tid)
            self.assertIsInstance(t, Tank)
            self.assertEqual(tank, t)
            
    def test_get_reservoir(self):
        for reservoir in self.model.network.reservoirs:
            rid = reservoir.id
            r = get_reservoir(self.model.network, rid)
            self.assertIsInstance(r, Reservoir)
            self.assertEqual(reservoir, r)
            
    def test_get_node(self):
        nodes = self.model.network.junctions + self.model.network.tanks + self.model.network.reservoirs
        for node in nodes:
            nid = node.id
            n = get_node(self.model.network, nid)
            self.assertIsInstance(n, Node)
            self.assertEqual(node, n)

    def test_get_pipe(self):
        for pipe in self.model.network.pipes:
            pid = pipe.id
            p = get_pipe(self.model.network, pid)
            self.assertIsInstance(p, Pipe)
            self.assertEqual(pipe, p)
            
    def test_get_pump(self):
        for pump in self.model.network.pumps:
            pid = pump.id
            p = get_pump(self.model.network, pid)
            self.assertIsInstance(p, Pump)
            self.assertEqual(pump, p)
            
    def test_get_valve(self):
        for valve in self.model.network.valves:
            vid = valve.id
            v = get_valve(self.model.network, vid)
            self.assertIsInstance(v, Valve)
            self.assertEqual(valve, v)
            
    def test_get_link(self):
        links = self.model.network.pipes + self.model.network.pumps + self.model.network.valves
        for link in links:
            lid = link.id
            l = get_link(self.model.network, lid)
            self.assertIsInstance(l, Link)
            self.assertEqual(link, l)

    def test_get_curve(self):
        for curve in self.model.network.curves:
            cid = curve.id
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

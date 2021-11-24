import unittest
from testing.base_cases import PoulakisEnhancedPDAModel
from oopnet.utils.adders.add_element import *
from oopnet.utils.getters.get_by_id import *


class PoulakisEnhancedPDAListTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = PoulakisEnhancedPDAModel()

    # todo: add tests that include patterns

    def test_add_simple_junction(self):
        self.assertEqual(self.model.n_junctions, len(self.model.network.junctions))
        add_junction(self.model.network, id='test', xcoordinate=1, ycoordinate=2, elevation=3, initialquality=0.1,
                     sourcequality=0.2, demand=10, comment='Test', emittercoefficient=0.2)
        self.assertEqual(self.model.n_junctions + 1, len(self.model.network.junctions))
        j = get_junction(self.model.network, 'test')
        self.assertEqual(1, j.xcoordinate)
        self.assertEqual(2, j.ycoordinate)
        self.assertEqual(3, j.elevation)
        self.assertEqual(0.1, j.initialquality)
        self.assertEqual(0.2, j.sourcequality)
        self.assertEqual(10, j.demand)
        self.assertEqual('Test', j.comment)
        self.assertEqual(0.2, j.emittercoefficient)        
        
    def test_add_simple_reservoir(self):
        self.assertEqual(self.model.n_reservoirs, len(self.model.network.reservoirs))
        add_reservoir(self.model.network, id='test', xcoordinate=1, ycoordinate=2, initialquality=0.1,
                      sourcequality=0.2, head=10, comment='Test')
        self.assertEqual(self.model.n_reservoirs + 1, len(self.model.network.reservoirs))
        r = get_reservoir(self.model.network, 'test')
        self.assertEqual(1, r.xcoordinate)
        self.assertEqual(2, r.ycoordinate)
        self.assertEqual(0.1, r.initialquality)
        self.assertEqual(0.2, r.sourcequality)
        self.assertEqual(10, r.head)
        self.assertEqual('Test', r.comment)

    def test_add_simple_tank(self):
        self.assertEqual(self.model.n_tanks, len(self.model.network.tanks))
        add_tank(self.model.network, id='test', xcoordinate=1, ycoordinate=2, elevation=3, initialquality=0.1,
                 sourcequality=0.2, comment='Test', initlevel=0.3, maxlevel=2.0, minlevel=0.1, minvolume=1.0)
        self.assertEqual(self.model.n_tanks + 1, len(self.model.network.tanks))
        t = get_tank(self.model.network, 'test')
        self.assertEqual(1, t.xcoordinate)
        self.assertEqual(2, t.ycoordinate)
        self.assertEqual(3, t.elevation)
        self.assertEqual(0.1, t.initialquality)
        self.assertEqual(0.2, t.sourcequality)
        self.assertEqual('Test', t.comment)
        self.assertEqual(0.3, t.initlevel)
        self.assertEqual(2.0, t.maxlevel)
        self.assertEqual(0.1, t.minlevel)
        self.assertEqual(1.0, t.minvolume)

    def test_add_simple_pipe(self):
        self.assertEqual(self.model.n_pipes, len(self.model.network.pipes))
        j1 = get_junction(self.model.network, 'J-20')
        j2 = get_junction(self.model.network, 'J-27')
        add_pipe(self.model.network, id='test', startnode=j1, endnode=j2, diameter=200, length=250, roughness=0.3,
                 minorloss=1.0, status='CLOSED', comment='Test')
        self.assertEqual(self.model.n_pipes + 1, len(self.model.network.pipes))
        p = get_pipe(self.model.network, 'test')
        self.assertEqual('J-20', p.startnode.id)
        self.assertEqual('J-27', p.endnode.id)
        self.assertEqual(200, p.diameter)
        self.assertEqual(250, p.length)
        self.assertEqual(0.3, p.roughness)
        self.assertEqual(1.0, p.minorloss)
        self.assertEqual('CLOSED', p.status)
        self.assertEqual('Test', p.comment)

    def test_add_simple_pump(self):
        self.assertEqual(self.model.n_pumps, len(self.model.network.pumps))
        j1 = get_junction(self.model.network, 'J-20')
        j2 = get_junction(self.model.network, 'J-27')
        add_pump(self.model.network, id='test', startnode=j1, endnode=j2, keyword='POWER', value=100, comment='Test')
        self.assertEqual(self.model.n_pumps + 1, len(self.model.network.pumps))
        p = get_pump(self.model.network, 'test')
        self.assertEqual('J-20', p.startnode.id)
        self.assertEqual('J-27', p.endnode.id)
        self.assertEqual('POWER', p.keyword)
        self.assertEqual(100, p.value)
        self.assertEqual('Test', p.comment)

    def test_add_simple_valve(self):
        self.assertEqual(self.model.n_valves, len(self.model.network.valves))
        j1 = get_junction(self.model.network, 'J-20')
        j2 = get_junction(self.model.network, 'J-27')
        add_valve(self.model.network, id='test', startnode=j1, endnode=j2, valvetype='TCV', diameter=150, minorloss=1.0,
                  comment='Test')
        self.assertEqual(self.model.n_valves + 1, len(self.model.network.valves))
        v = get_valve(self.model.network, 'test')
        self.assertEqual('J-20', v.startnode.id)
        self.assertEqual('J-27', v.endnode.id)
        self.assertEqual('TCV', v.valvetype)
        self.assertEqual(150, v.diameter)
        self.assertEqual(1.0, v.minorloss)
        self.assertEqual('Test', v.comment)


if __name__ == '__main__':
    unittest.main()

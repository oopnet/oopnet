import unittest

from oopnet.utils.getters import *
from oopnet.utils.removers import *

from testing.base import SimpleModel


class SimpleRemovalTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_remove_junction(self):
        remove_id = 'J-1'
        remove_junction(self.model.network, remove_id)
        ids = get_junction_ids(self.model.network)
        self.assertFalse(remove_id in ids)
        self.assertEqual(self.model.n_junctions - 1, len(self.model.network._nodes['junctions']))

    def test_remove_tank(self):
        remove_id = 'T-1'
        remove_tank(self.model.network, remove_id)
        ids = get_tank_ids(self.model.network)
        self.assertFalse(remove_id in ids)
        self.assertEqual(self.model.n_tanks - 1, len(self.model.network._nodes['tanks']))

    def test_remove_reservoir(self):
        remove_id = 'R-1'
        remove_reservoir(self.model.network, remove_id)
        ids = get_reservoir_ids(self.model.network)
        self.assertFalse(remove_id in ids)
        self.assertEqual(self.model.n_reservoirs - 1, len(self.model.network._nodes['reservoirs']))

    def test_remove_pipe(self):
        remove_id = 'P-1'
        remove_pipe(self.model.network, remove_id)
        ids = get_pipe_ids(self.model.network)
        self.assertFalse(remove_id in ids)
        self.assertEqual(self.model.n_pipes - 1, len(self.model.network._links['pipes']))

    def test_remove_pump(self):
        remove_id = 'PU-1'
        remove_pump(self.model.network, remove_id)
        ids = get_pump_ids(self.model.network)
        self.assertFalse(remove_id in ids)
        self.assertEqual(self.model.n_pumps - 1, len(self.model.network._links['pumps']))

    def test_remove_valve(self):
        remove_id = 'V-1'
        remove_valve(self.model.network, remove_id)
        ids = get_junction_ids(self.model.network)
        self.assertFalse(remove_id in ids)
        self.assertEqual(self.model.n_valves - 1, len(self.model.network._links['valves']))

    def test_remove_node(self):
        remove_ids = ['J-1', 'T-1', 'R-1']

        for remove_id in remove_ids:
            remove_node(self.model.network, remove_id)
            ids = get_node_ids(self.model.network)
            self.assertFalse(remove_id in ids)

    def test_remove_link(self):
        remove_ids = ['P-1', 'PU-1', 'V-1']

        for remove_id in remove_ids:
            remove_link(self.model.network, remove_id)
            ids = get_link_ids(self.model.network)
            self.assertFalse(remove_id in ids)


if __name__ == '__main__':
    unittest.main()

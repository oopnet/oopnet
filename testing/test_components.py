import unittest
from copy import deepcopy

import numpy as np

from oopnet.utils.getters.get_by_id import get_link, get_pipe
from oopnet.utils.getters.element_lists import get_link_ids, get_junction_ids, get_pipe_ids

from testing.base import SimpleModel


class TestLink(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()
        p = get_pipe(self.model.network, 'P-0')
        s = p.startnode
        e = p.endnode
        s.xcoordinate, s.ycoordinate, s.elevation = 1, 1, 1
        e.xcoordinate, e.ycoordinate, e.elevation = 3, 3, 3
        self._test_pipe = p
        self._original_pipe = deepcopy(p)
        self._start = deepcopy(s)
        self._end = deepcopy(e)

    def test_revert(self):
        p = get_link(self.model.network, 'P-0')
        self.assertEqual('J-1', p.startnode.id)  # add assertion here
        self.assertEqual('T-1', p.endnode.id)
        p.revert()
        self.assertEqual('T-1', p.startnode.id)  # add assertion here
        self.assertEqual('J-1', p.endnode.id)

    def test_rename(self):
        p = get_link(self.model.network, 'P-0')
        self.assertTrue('P-0' in get_link_ids(self.model.network))
        p.id = 'new-ID'
        self.assertTrue('new-ID' in get_link_ids(self.model.network))

    def _split_test(self, new_junction, new_pipe, ratio):
        coords = np.add(self._start.coordinates, self._end.coordinates) * ratio
        self.assertIsNone(np.testing.assert_array_equal(coords, new_junction.coordinates))
        self.assertFalse(id(new_pipe) == id(self._test_pipe))
        self.assertEqual(self._original_pipe.roughness, new_pipe.roughness)
        self.assertEqual(self._original_pipe.length * ratio, new_pipe.length)
        self.assertTrue(new_junction.id in get_junction_ids(self.model.network))
        self.assertTrue(new_pipe.id in get_pipe_ids(self.model.network))

    def test_split_simple(self):
        new_j, new_p = self._test_pipe.split()
        self._split_test(new_j, new_p, 0.5)

    def test_split_low(self):
        for ratio in [-np.inf, -1, 0]:
            with self.assertRaises(ValueError):
                self._test_pipe.split(split_ratio=ratio)

    def test_split_high(self):
        for ratio in [np.inf, 2, 1]:
            with self.assertRaises(ValueError):
                self._test_pipe.split(split_ratio=ratio)


if __name__ == '__main__':
    unittest.main()

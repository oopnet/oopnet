import unittest

from oopnet.utils.getters.get_by_id import get_link, get_pipe
from oopnet.utils.getters.element_lists import get_link_ids

from testing.base import SimpleModel


class TestLink(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

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

    def test_split_simple(self):
        p = get_pipe(self.model.network, 'P-0')
        p.split()


if __name__ == '__main__':
    unittest.main()

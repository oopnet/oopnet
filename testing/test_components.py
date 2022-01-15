import unittest

from oopnet.utils.getters import get_link, get_link_ids

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
        self.assertIsInstance(p._component_hash, dict)
        self.assertTrue('P-0' in get_link_ids(self.model.network))
        p.id = 'new-ID'
        self.assertTrue('new-ID' in get_link_ids(self.model.network))


if __name__ == '__main__':
    unittest.main()

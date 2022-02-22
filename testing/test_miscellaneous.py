import unittest
import pickle

from testing.base import CTownModel


class PickleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = CTownModel()

    def test_pickle_network(self):
        dump = pickle.dumps(self.model.network)
        new_network = pickle.loads(dump)
        self.assertEqual(self.model.network, new_network)

    def test_pickle_report(self):
        import xarray as xr
        rpt = self.model.network.run()
        dump = pickle.dumps(rpt)
        new_rpt = pickle.loads(dump)
        xr.testing.assert_equal(rpt.nodes, new_rpt.nodes)
        xr.testing.assert_equal(rpt.links, new_rpt.links)


if __name__ == '__main__':
    unittest.main()

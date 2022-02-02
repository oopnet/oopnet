import unittest

import pandas as pd

from oopnet.utils.getters import *

from testing.base import SimpleModel


class SimplePropertyGetterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.model = SimpleModel()

    def test_get_startnodes(self):
        startnodes = get_startnodes(self.model.network)
        self.assertIsInstance(startnodes, pd.Series)
        self.assertEqual(self.model.n_links, len(startnodes))

    def test_get_endnodes(self):
        endnodes = get_endnodes(self.model.network)
        self.assertIsInstance(endnodes, pd.Series)
        self.assertEqual(self.model.n_links, len(endnodes))

    def test_get_startendnodes(self):
        startendnodes = get_startendnodes(self.model.network)
        self.assertIsInstance(startendnodes, pd.DataFrame)
        self.assertEqual(self.model.n_links, len(startendnodes))

    def test_get_startendcoordinates(self):
        coords = get_startendcoordinates(self.model.network)
        self.assertIsInstance(coords, pd.DataFrame)
        self.assertEqual(self.model.n_links, len(coords))

    # def test_get_initialstatus(self):
    #     status = get_initialstatus(self.model.network)
    #     self.assertIsInstance(status, pd.Series)
    #     self.assertEqual(self.model.n_pumps + self.model.n_valves, len(status))

    def test_get_status(self):
        status = get_status(self.model.network)
        self.assertIsInstance(status, pd.Series)
        self.assertEqual(self.model.n_links, len(status))

    def test_get_settings(self):
        settings = get_setting(self.model.network)
        self.assertIsInstance(settings, pd.Series)
        self.assertEqual(self.model.n_valves + self.model.n_pumps, len(settings))

    def test_get_linkcenter_coordinates(self):
        coords = get_linkcenter_coordinates(self.model.network)
        self.assertIsInstance(coords, pd.DataFrame)
        self.assertEqual(self.model.n_links, len(coords))

    def test_get_link_comment(self):
        comments = get_link_comment(self.model.network)
        self.assertIsInstance(comments, pd.Series)
        self.assertEqual(self.model.n_links, len(comments))

    def test_get_length(self):
        length = get_length(self.model.network)
        self.assertIsInstance(length, pd.Series)
        self.assertEqual(self.model.n_pipes, len(length))

    def test_get_diameter(self):
        diameter = get_diameter(self.model.network)
        self.assertIsInstance(diameter, pd.Series)
        self.assertEqual(self.model.n_pipes + self.model.n_valves, len(diameter))

    def test_get_roughness(self):
        roughness = get_roughness(self.model.network)
        self.assertIsInstance(roughness, pd.Series)
        self.assertEqual(self.model.n_pipes, len(roughness))

    def test_get_minorloss(self):
        minorloss = get_minorloss(self.model.network)
        self.assertIsInstance(minorloss, pd.Series)
        self.assertEqual(self.model.n_pipes, len(minorloss))

    def test_get_xcoordinate(self):
        coords = get_xcoordinate(self.model.network)
        self.assertIsInstance(coords, pd.Series)
        self.assertEqual(self.model.n_nodes, len(coords))

    def test_get_ycoordinate(self):
        coords = get_ycoordinate(self.model.network)
        self.assertIsInstance(coords, pd.Series)
        self.assertEqual(self.model.n_nodes, len(coords))

    def test_get_coordinates(self):
        coords = get_coordinates(self.model.network)
        self.assertIsInstance(coords, pd.DataFrame)
        self.assertEqual(self.model.n_nodes, len(coords))

    def test_get_elevation(self):
        elev = get_elevation(self.model.network)
        self.assertIsInstance(elev, pd.Series)
        self.assertEqual(self.model.n_nodes, len(elev))

    def test_get_basedemand(self):
        demand = get_basedemand(self.model.network)
        self.assertIsInstance(demand, pd.Series)
        self.assertEqual(self.model.n_junctions, len(demand))

    def test_get_comment(self):
        comment = get_node_comment(self.model.network)
        self.assertIsInstance(comment, pd.Series)
        self.assertEqual(self.model.n_nodes, len(comment))

if __name__ == '__main__':
    unittest.main()

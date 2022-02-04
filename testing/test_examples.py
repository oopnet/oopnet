import unittest
import os
import shutil
from unittest.mock import patch

from matplotlib import pyplot as plt

from base import set_dir_examples, set_dir_testing


@patch('matplotlib.pyplot.show')
class ExampleTest(unittest.TestCase):

    def setUp(self) -> None:
        set_dir_examples()

    def tearDown(self) -> None:
        to_delete = ['bokehexample.html', 'oopnet.log']
        for file in to_delete:
            if os.path.isfile(file):
                os.remove(file)

        if os.path.isdir('tmp'):
            shutil.rmtree('tmp')
        set_dir_testing()
        try:
            plt.close('all')
        except:
            pass

    def test_adders_and_removers(self, mock_show):
        import examples.adders_and_removers

    def test_adjacency_matrix(self, mock_show):
        import examples.adjacency_matrix

    @patch('bokeh.plotting.show')
    def test_bokeh_run_and_plot(self, mock_show_plt, mock_show_bokeh):
        import examples.bokeh_run_and_plot

    def test_centrality(self, mock_show):
        import examples.centrality

    def test_edge_centrality(self, mock_show):
        import examples.edge_centrality

    def test_extended_period(self, mock_show):
        import examples.extended_period

    def test_graph_stuff(self, mock_show):
        import examples.graph_stuff

    def test_mc_make_some_noise(self, mock_show):
        import examples.mc_make_some_noise

    def test_mc_stereo_multiprocessing(self, mock_show):
        import examples.mc_stereo_multiprocessing

    def test_mc_stereo_scoop(self, mock_show):
        import examples.mc_stereo_scoop

    def test_miscellaneous(self, mock_show):
        import examples.miscellaneous

    def test_read_and_run(self, mock_show):
        import examples.read_and_run

    def test_report_settings(self, mock_show):
        import examples.report_settings

    def test_run_and_plot(self, mock_show):
        import examples.run_and_plot

    def test_test(self, mock_show):
        import examples.test


if __name__ == '__main__':
    unittest.main()

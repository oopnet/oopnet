import unittest
import os
import shutil
from unittest.mock import patch

from matplotlib import pyplot as plt

from testing.base import set_dir_examples, set_dir_testing


@patch('matplotlib.pyplot.show')
class ExampleTest(unittest.TestCase):

    def setUp(self) -> None:
        set_dir_examples()

    def tearDown(self) -> None:
        to_delete = ['bokehexample.html', 'oopnet.log', 'simple_animation.gif', 'new_model.inp']
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

    def test_error_handling(self, mock_show):
        import examples.error_handling

    def test_graph_weight(self, mock_show):
        import examples.graph_weight

    # def test_logs(self, mock_show):
    #     try:
    #         import examples.logs
    #     except TypeError:
    #         pass

    def test_mc_make_some_noise(self, mock_show):
        import examples.mc_make_some_noise

    def test_mc_stereo_multiprocessing(self, mock_show):
        import examples.mc_stereo_multiprocessing

    # def test_mc_stereo_scoop(self, mock_show):
    #     import examples.mc_stereo_scoop

    def test_miscellaneous(self, mock_show):
        import examples.miscellaneous

    def test_run_and_animate(self, mock_show):
        import examples.run_and_animate

    def test_test(self, mock_show):
        import examples.test
        
    def test_userguide_network(self, mock_show):
        import examples.userguide_network

    def test_userguide_graphs(self, mock_show):
        import examples.userguide_graphs

    def test_userguide_plotting(self, mock_show):
        import examples.userguide_plotting

    def test_userguide_settings(self, mock_show):
        import examples.userguide_settings

    def test_userguide_simulations(self, mock_show):
        import examples.userguide_simulating

    def test_run_and_animate(self, mock_show):
        import examples.run_and_animate



if __name__ == '__main__':
    unittest.main()

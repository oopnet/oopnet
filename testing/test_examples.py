import unittest
import os
import shutil

from base import set_dir_examples, set_dir_testing


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

    def test_adders_and_removers(self):
        import examples.adders_and_removers

    def test_adjacency_matrix(self):
        import examples.adjacency_matrix

    def test_bokeh_run_and_plot(self):
        import examples.bokeh_run_and_plot

    def test_centrality(self):
        import examples.centrality

    def test_edge_centrality(self):
        import examples.edge_centrality

    def test_extended_period(self):
        import examples.extended_period

    def test_graph_stuff(self):
        import examples.graph_stuff

    def test_mc_make_some_noise(self):
        import examples.mc_make_some_noise

    def test_mc_stereo_multiprocessing(self):
        import examples.mc_stereo_multiprocessing

    def test_mc_stereo_scoop(self):
        import examples.mc_stereo_scoop

    def test_miscellaneous(self):
        import examples.miscellaneous

    def test_read_and_run(self):
        import examples.read_and_run

    def test_report_settings(self):
        import examples.report_settings

    def test_run_and_plot(self):
        import examples.run_and_plot

    def test_test(self):
        import examples.test


if __name__ == '__main__':
    unittest.main()

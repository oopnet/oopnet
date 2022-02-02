import timeit
from os import remove, path
from dataclasses import dataclass
from typing import Optional

from matplotlib import pyplot as plt

from oopnet.elements.network import Network
from oopnet.api import *

poulakis_filename = path.join('testing', 'networks', 'Poulakis_enhanced_PDA.inp')
ctown_filename = path.join('examples', 'data', 'C-town.inp')


@dataclass
class OOPNETBenchmark:
    filename: str
    network: Optional[Network] = None

    def __post_init__(self):
        self.reset()

    def reset(self):
        self.network = Read(self.filename)

    def read(self):
        network = Read(self.filename)

    def increase_demand(self):
        for j in get_junctions(self.network):
            j.demand += 0.0001

    def change_length(self):
        for p in get_pipes(self.network):
            p.length -= 0.0001

    def random_node_access(self):
        rng = np.random.default_rng(2021)
        nids = get_node_ids(self.network)
        rng.shuffle(nids)

        for nid in nids:
            n = get_node(self.network, nid)
            n.xcoordinate, n.ycoordinate = (0, 0)

    def random_link_access(self):
        rng = np.random.default_rng(2021)
        lids = get_link_ids(self.network)
        rng.shuffle(lids)

        for lid in lids:
            l = get_link(self.network, lid)
            l.status = 1

    def lookup_ids(self):
        for node in get_nodes(self.network):
            id = node.id

        for link in get_links(self.network):
            id = link.id

    def create_graph(self):
        g = MultiGraph(self.network)

    def simulate(self):
        rpt = Run(self.network)

    def write(self):
        Write(self.network, 'test.inp')
        remove('test.inp')

    def plot(self):
        Plot(self.network)
        plt.close()

    def run_single_instance(self):
        # self.read()
        # self.increase_demand()
        # self.change_length()
        # self.random_node_access()
        # self.random_link_access()
        # self.lookup_ids()
        self.create_graph()
        # self.simulate()
        # self.write()

    def run_bechmark(self, n):
        print(f'Running benchmark for {path.split(self.filename)[-1]}')

        print('Reading file')
        print(np.mean(timeit.Timer(stmt=self.read).repeat(number=n)))
        self.reset()

        print('\nChanging demands')
        print(np.mean(timeit.Timer(stmt=self.increase_demand).repeat(number=n)))
        self.reset()

        print('\nChanging lengths')
        print(np.mean(timeit.Timer(stmt=self.change_length).repeat(number=n)))
        self.reset()

        print('\nRandomly accessing Nodes')
        print(np.mean(timeit.Timer(stmt=self.random_node_access).repeat(number=n)))
        self.reset()

        print('\nRandomly accessing Links')
        print(np.mean(timeit.Timer(stmt=self.random_link_access).repeat(number=n)))
        self.reset()

        print('\nLookup Node and Link IDs')
        print(np.mean(timeit.Timer(stmt=self.lookup_ids).repeat(number=n)))
        self.reset()

        print('\nGenerating MultiGraph')
        print(np.mean(timeit.Timer(stmt=self.create_graph).repeat(number=n)))
        self.reset()

        print('\nSimulating model')
        print(np.mean(timeit.Timer(stmt=self.simulate).repeat(number=n)))
        self.reset()

        print('\nWriting file')
        print(np.mean(timeit.Timer(stmt=self.write).repeat(number=n)))
        self.reset()

        print('\nPlotting network')
        print(np.mean(timeit.Timer(stmt=self.plot).repeat(number=n)))
        self.reset()


if __name__ == '__main__':
    n = 1_000
    filename = ctown_filename
    OOPNETBenchmark(filename=filename).run_bechmark(n)
    # OOPNETBenchmark(filename=filename).run_single_instance()

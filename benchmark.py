import timeit
from os import remove, path

from dataclasses import dataclass

from oopnet.api import *
from oopnet.elements.network import Network

filename = path.join('testing', 'networks', 'Poulakis_enhanced_PDA.inp')
n = 1_000


@dataclass
class OOPNETBenchmark:
    filename: str

    def read(self):
        self.network = Read(self.filename)

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
            n.comment = 'Test'

    def random_link_access(self):
        rng = np.random.default_rng(2021)
        lids = get_link_ids(self.network)
        rng.shuffle(lids)

        for lid in lids:
            l = get_link(self.network, lid)
            l.comment = 'Test'

    def simulate(self):
        rpt = Run(self.network)

    def write(self):
        Write(self.network, 'test.inp')
        remove('test.inp')

    def run_single_instance(self):
        self.read()
        self.increase_demand()
        self.change_length()
        self.simulate()
        self.write()

    def run_bechmark(self):
        print('Reading file')
        print(np.mean(timeit.Timer(stmt=self.read).repeat(number=n)))

        print('Changing demands')
        print(np.mean(timeit.Timer(stmt=self.increase_demand).repeat(number=n)))

        print('Changing lengths')
        print(np.mean(timeit.Timer(stmt=self.change_length).repeat(number=n)))

        print('Randomly accessing Nodes')
        print(np.mean(timeit.Timer(stmt=self.random_node_access).repeat(number=n)))

        print('Randomly accessing Links')
        print(np.mean(timeit.Timer(stmt=self.random_link_access).repeat(number=n)))

        print('Simulating model')
        print(np.mean(timeit.Timer(stmt=self.simulate).repeat(number=n)))

        print('Writing file')
        print(np.mean(timeit.Timer(stmt=self.write).repeat(number=n)))


if __name__ == '__main__':
    OOPNETBenchmark(filename=filename).run_bechmark()
    # OOPNETBenchmark(filename=filename).run_single_instance()


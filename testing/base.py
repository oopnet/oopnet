import os
import pathlib
from typing import List

from oopnet.elements.network import Network
from oopnet.elements.network_components import Junction, Pipe, Tank, Reservoir, Pump, Valve, PRV
from oopnet.elements.system_operation import Curve
from oopnet.utils.adders.add_element import add_junction, add_pipe, add_node, add_curve, add_link
from oopnet.utils.getters.get_by_id import get_node, get_curve, get_junction


def add_dummy_junctions(network: Network, n: int) -> Network:
    for i in range(1, n+1):
        j = Junction(id=f'J-{i}', demand=10.0)
        add_junction(network, j)
    return network


def add_dummy_pipes(network: Network, connectivity: List[tuple[str, str]]) -> Network:
    for index, ids in enumerate(connectivity):
        start_id, end_id = ids
        p = Pipe(id=f'P-{index}', diameter=200.0, roughness=0.1, startnode=get_node(network, start_id),
                 endnode=get_node(network, end_id))
        add_pipe(network, p)
    return network


def create_dummy_spa_network() -> Network:
    """
    Creates a Single Period Analysis network that is prefilled with at least one component of every type.
    """

    network = Network()
    add_dummy_junctions(network, 3)
    t = Tank(id='T-1')
    r = Reservoir(id='R-1', head=50.0)
    j = get_junction(network, 'J-1')
    j.demand = -1

    for obj in [t, r]:
        add_node(network, obj)

    c = Curve(id='C-1', xvalues=[10, 15], yvalues=[15, 10])
    add_curve(network, c)

    add_dummy_pipes(network, [('J-1', 'T-1'), ('J-1', 'R-1')])
    pu = Pump(id='PU-1', head=get_curve(network, 'C-1'), startnode=get_node(network, 'J-1'),
              endnode=get_node(network, 'J-2'))
    v = PRV(id='V-1', setting=5.0, startnode=get_node(network, 'J-1'),
            endnode=get_node(network, 'J-3'))

    for obj in [pu, v]:
        add_link(network, obj)
    return network


class TestModel:
    """Class for testing models.

    Attributes:
        network: OOPNET network object
        n_junctions: number of junctions in network
        n_tanks: number of tanks in network
        n_reservoirs: number of reservoirs in network
        n_pipes: number of pipes in network
        n_valves: number of valves in network
        n_pumps: number of pumps in network

    """
    network: Network
    n_junctions: int = 0
    n_tanks: int = 0
    n_reservoirs: int = 0
    n_pipes: int = 0
    n_valves: int = 0
    n_pumps: int = 0
    n_controls: int = 0
    n_rules: int = 0
    n_curves: int = 0
    n_patterns: int = 0

    @property
    def n_nodes(self) -> int:
        """Total number of nodes in network."""
        return self.n_junctions + self.n_tanks + self.n_reservoirs

    @property
    def n_links(self) -> int:
        """Total number of links in network."""
        return self.n_pipes + self.n_pumps + self.n_valves

    def __init__(self):
        set_dir_testing()


class SimpleModel(TestModel):
    n_junctions = 3
    n_tanks = 1
    n_reservoirs = 1
    n_pipes = 2
    n_valves = 1
    n_pumps = 1

    def __init__(self):
        super().__init__()
        self.network = create_dummy_spa_network()


class PoulakisEnhancedPDAModel(TestModel):
    n_junctions = 30
    n_tanks = 1
    n_reservoirs = 1
    n_pipes = 51
    n_valves = 6
    n_pumps = 1

    def __init__(self):
        super().__init__()
        self.network = Network.read(os.path.join('networks', 'Poulakis_enhanced_PDA.inp'))


class CTownModel(TestModel):
    n_junctions = 388
    n_tanks = 7
    n_reservoirs = 1
    n_pipes = 432
    n_valves = 1
    n_pumps = 11

    def __init__(self):
        super().__init__()
        self.network = Network.read(os.path.join('..', 'examples', 'data', 'C-town.inp'))
        print()


class MicropolisModel(TestModel):
    n_junctions = 1574
    n_tanks = 1
    n_reservoirs = 2
    n_pipes = 1415
    n_valves = 196
    n_controls = 0
    n_pumps = 8
    n_rules = 7
    n_curves = 5
    n_patterns = 7

    def __init__(self):
        super().__init__()
        self.network = Network.read(os.path.join('..', 'examples', 'data', 'MICROPOLIS_v1.inp'))


class RulesModel(TestModel):
    n_junctions = 1
    n_tanks = 1
    n_reservoirs = 1
    n_pipes = 2
    n_valves = 0
    n_controls = 0
    n_pumps = 1
    n_rules = 2
    n_curves = 1
    n_patterns = 0

    def __init__(self):
        super().__init__()
        self.network = Network.read(os.path.join('networks', 'Rules_network.inp'))


class ETownModel(TestModel):
    n_junctions = 11075
    n_tanks = 17
    n_reservoirs = 5
    n_pipes = 13913
    n_valves = 11
    n_controls = 0
    n_pumps = 3
    n_rules = 0
    n_curves = 3
    n_patterns = 1

    def __init__(self):
        super().__init__()
        self.network = Network.read(os.path.join('..', 'examples', 'data', 'ETown.inp'))


def set_dir_examples():
    file_dir = pathlib.Path(__file__).parent.absolute()
    os.chdir(file_dir.parent / 'examples')
    print(os.getcwd())


def set_dir_testing():
    file_dir = pathlib.Path(__file__)
    os.chdir(file_dir.parent)


def activate_all_report_parameters(network: Network):
    for param in network.reportparameter.__dict__.keys():
        setattr(network.reportparameter, param, 'YES')


if __name__ == '__main__':
    network = PoulakisEnhancedPDAModel().network
    from oopnet.plotter.pyplot import Plotsimulation as Plot
    from matplotlib import pyplot as plt
    fig, ax = plt.subplots(figsize=(15, 15))
    rpt = network.run()
    Plot(network, ax=ax, links=rpt.flow)
    plt.show()

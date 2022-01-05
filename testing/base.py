from os.path import join
from typing import List

from oopnet.elements.base import PumpKeyword, ValveType
from oopnet.elements.network import Network
from oopnet.elements.network_components import Junction, Pipe, Tank, Reservoir, Pump, Valve
from oopnet.elements.system_operation import Curve
from oopnet.reader.decorator_reader.read import read as Read
from oopnet.utils.adders.add_element import add_junction, add_pipe, add_node, add_curve, add_link
from oopnet.utils.getters.get_by_id import get_node


def add_dummy_junctions(network: Network, n: int) -> Network:
    for i in range(1, n+1):
        j = Junction(id=f'J-{i}', demand=10)
        add_junction(network, j)
    return network


def add_dummy_pipes(network: Network, connectivity: List[tuple]) -> Network:
    for index, ids in enumerate(connectivity):
        start_id, end_id = ids
        p = Pipe(id=f'P-{index}', diameter=200, roughness=0.1, startnode=get_node(network, start_id),
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
    r = Reservoir(id='R-1', head=50)

    for obj in [t, r]:
        add_node(network, obj)

    c = Curve(id='C-1', xvalues=[10, 15], yvalues=[15, 10])
    add_curve(network, c)

    add_dummy_pipes(network, [('J-1', 'T-1'), ('J-1', 'R-1')])
    pu = Pump(id='PU-1', keyword=PumpKeyword.HEAD, value='C-1', startnode=get_node(network, 'J-1'),
              endnode=get_node(network, 'J-2'))
    v = Valve(id='V-1', valvetype=ValveType.PRV, setting=5, startnode=get_node(network, 'J-1'),
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


class SimpleModel(TestModel):
    n_junctions = 3
    n_tanks = 1
    n_reservoirs = 1
    n_pipes = 2
    n_valves = 1
    n_pumps = 1

    def __init__(self):
        self.network = create_dummy_spa_network()


class PoulakisEnhancedPDAModel(TestModel):
    n_junctions = 30
    n_tanks = 1
    n_reservoirs = 1
    n_pipes = 51
    n_valves = 6
    n_pumps = 1

    def __init__(self):
        self.network = Read(join('networks', 'Poulakis_enhanced_PDA.inp'))


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
        self.network = Read(join('..', 'examples', 'data', 'MICROPOLIS_v1.inp'))


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
        self.network = Read(join('networks', 'Rules_network.inp'))


if __name__ == '__main__':
    from oopnet.api import *
    network = MicropolisModel()
    rpt = Run(network.network, output=True, delete=False)
    # rpt2 = Run(thing=join('networks', 'Poulakis_enhanced_PDA.inp'), output=True, delete=False)

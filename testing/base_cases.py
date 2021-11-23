from oopnet.api import Read
import os
import sys

os.chdir(sys.path[0])


class PoulakisEnhancedPDAModel:
    network = Read(os.path.join('testing', 'networks', 'Poulakis_enhanced_PDA.inp'))
    n_junctions = 30
    n_tanks = 1
    n_reservoirs = 1
    n_pipes = 51
    n_valves = 6
    n_pumps = 1
    n_nodes = n_junctions + n_tanks + n_reservoirs
    n_links = n_pipes + n_pumps + n_valves

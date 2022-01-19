import os

from oopnet import *

filename = os.path.join('data', 'Poulakis.inp')

net = Read(filename)

add_junction(net, Junction(id='unconnected'))

try:
    rpt = Run(net)
except EPANETSimulationError as e:
    print(e)

    if e.check_contained_errors(UnconnectedNodeError):
        print('Caught UnconnectedNodeError')
    if e.check_contained_errors(InputDataError):
        print('Caught InputDataError')
    if any(e.check_contained_errors([InputDataError, UnconnectedNodeError])):
        print('Caught UnconnectedNodeError and InputDataError')

net = Read(filename)
p = get_pipe(net, 'P-01')
p.length = -100.0

try:
    rpt = Run(net)
except EPANETSimulationError as e:
    print(e)

    if e.check_contained_errors(IllegalLinkPropertyError):
        print('Illegal property encountered')

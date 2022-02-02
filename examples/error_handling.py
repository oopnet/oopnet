import os

import oopnet as on

filename = os.path.join('data', 'Poulakis.inp')

net = on.Read(filename)

on.add_junction(net, on.Junction(id='unconnected'))

try:
    rpt = on.Run(net)
except on.EPANETSimulationError as e:
    print(e)

    if e.check_contained_errors(on.UnconnectedNodeError):
        print('Caught UnconnectedNodeError')
    if e.check_contained_errors(on.InputDataError):
        print('Caught InputDataError')
    if any(e.check_contained_errors([on.InputDataError, on.UnconnectedNodeError])):
        print('Caught UnconnectedNodeError and InputDataError')

net = on.Read(filename)
p = on.get_pipe(net, 'P-01')
p.length = -100.0

try:
    rpt = on.Run(net)
except on.EPANETSimulationError as e:
    print(e)

    if e.check_contained_errors(on.IllegalLinkPropertyError):
        print('Illegal property encountered')

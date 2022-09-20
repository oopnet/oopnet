import os

import oopnet as on

blank_network = on.Network()

filename = os.path.join('data', 'Poulakis.inp')
network = on.Network.read(filename)

network.write('new_model.inp')

for j in on.get_junctions(network):
    print(j, j.demand, j.elevation)

on.add_junction(network=network, junction=on.Junction(id='J-32', xcoordinate=5500, ycoordinate=8000, demand=80))

on.add_pipe(network=network, pipe=on.Pipe(id='P-51', length=1000, diameter=400, roughness=0.26,
                                          startnode=on.get_node(network, 'J-32'), endnode=on.get_node(network, 'J-26')))

rjid = 'J-24'
rj = on.get_node(network, rjid)
neighbor_links = on.get_adjacent_links(network, rj)

for neighbour in neighbor_links:
    on.remove_pipe(network=network, id=neighbour.id)

on.remove_junction(network=network, id=rjid)

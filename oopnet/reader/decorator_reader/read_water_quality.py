from .decorators import section_reader
from ...elements.water_quality import Reaction


@section_reader('QUALITY', 3)
def read_quality(network, block):
    for vals in block:
        vals = vals['values']
        j = network.networkhash['node'][vals[0]]
        if len(vals) > 1:
            j.initialquality = float(vals[1])


@section_reader('REACTIONS', 3)
def read_reaction(network, block):
    for vals in block:
        vals = vals['values']
        if network.reactions is None:
            network.reactions = Reaction()
        r = network.reactions
        vals[0] = vals[0].upper()
        if vals[0] == 'ORDER':
            vals[1] = vals[1].upper()
            if vals[1] == 'BULK':
                r.orderbulk = float(vals[2])
            elif vals[1] == 'WALL':
                r.orderwall = float(vals[2])
            elif vals[1] == 'TANK':
                r.ordertank = float(vals[2])
        elif vals[0] == 'GLOBAL':
            vals[1] = vals[1].upper()
            if vals[1] == 'BULK':
                r.globalbulk = float(vals[2])
            elif vals[1] == 'WALL':
                r.globalwall = float(vals[2])
        elif vals[0] == 'LIMITING' and vals[1].upper() == 'POTENTIAL':
            r.limitingpotential = float(vals[2])
        elif vals[0] == 'ROUGHNESS' and vals[1].upper() == 'CORRELATION':
            r.limitingpotential = float(vals[2])
        elif vals[0] == 'BULK':
            p = network.networkhash['link'][vals[1]]
            p.reactionbulk = float(vals[2])
            if r.bulk is None:
                r.bulk = [p]
            else:
                r.bulk.append(p)
        elif vals[0] == 'WALL':
            p = network.networkhash['link'][vals[1]]
            p.reactionwall = float(vals[2])
            if r.wall is None:
                r.wall = [p]
            else:
                r.wall.append(p)
        elif vals[0] == 'TANK':
            p = network.networkhash['link'][vals[1]]
            p.reactiontank = float(vals[2])
            if r.tank is None:
                r.tank = [p]
            else:
                r.tank.append(p)


@section_reader('SOURCES', 3)
def read_sources(network, block):
    for vals in block:
        vals = vals['values']
        n = network.networkhash['node'][vals[0]]
        # network.networkhash['source'][vals[0]] = n
        if len(vals) > 1:
            n.sourcetype = vals[1].upper()
        if len(vals) > 2:
            n.strength = float(vals[2])
        if len(vals) > 3:
            n.sourcepattern = network.networkhash['pattern'][vals[3]]


@section_reader('MIXING', 3)
def read_mixing(network, block):
    for vals in block:
        vals = vals['values']
        t = network.networkhash['node'][vals[0]]
        # network.networkhash['mixing'][vals[0]] = t
        if len(vals) > 1:
            t.mixingmodel = vals[1].upper()
        if len(vals) > 2:
            t.compartmentvolume = float(vals[2])

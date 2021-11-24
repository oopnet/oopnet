from .decorators import section_reader
from ...elements.network_components import *
from ...elements.system_operation import Pattern
from ...utils.getters.get_by_id import get_node, get_junction, get_pattern, get_curve


@section_reader('TITLE', 4)
def read_title(network, block):
    for vals in block:
        vals = vals['values']
        network.title = " ".join(vals)


@section_reader('JUNCTIONS', 1)
def read_junction(network, block):
    for vals in block:
        comment = vals['comments'] or None
        vals = vals['values']
        j = Junction(id=vals[0], comment=comment, tag=None)
        if len(vals) > 1:
            j.elevation = float(vals[1])
        if len(vals) > 2:
            j.demand = float(vals[2])
        if len(vals) > 3:
            p = get_pattern(network, vals[3])
            j.demandpattern = p
        network.junctions.append(j)


@section_reader('RESERVOIRS', 1)
def read_reservoir(network, block):
    for vals in block:
        comment = vals['comments'] or None
        vals = vals['values']
        r = Reservoir(id=vals[0], comment=comment, tag=None)
        if len(vals) > 1:
            r.head = float(vals[1])
        if len(vals) > 2:
            r.headpattern = Pattern(id=vals[2])
        network.reservoirs.append(r)


@section_reader('TANKS', 1)
def read_tanks(network, block):
    for vals in block:
        comment = vals['comments'] or None
        vals = vals['values']
        t = Tank(id=vals[0], comment=comment, tag=None)
        if len(vals) > 1:
            t.elevation = float(vals[1])
        if len(vals) > 2:
            t.initlevel = float(vals[2])
        if len(vals) > 3:
            t.minlevel = float(vals[3])
        if len(vals) > 4:
            t.maxlevel = float(vals[4])
        if len(vals) > 5:
            t.diam = float(vals[5])
        if len(vals) > 6:
            t.minvolume = float(vals[6])
        if len(vals) > 7:
            c = get_curve(network, vals[7])
            t.volumecurve = c
        network.tanks.append(t)


@section_reader('PIPES', 2)
def read_pipes(network, block):
    for vals in block:
        comment = vals['comments'][0] if vals['comments'] else None
        vals = vals['values']

        p = Pipe(id=vals[0], comment=comment, tag=None)
        if len(vals) > 1:
            j = get_node(network, vals[1])
            p.startnode = j
        if len(vals) > 2:
            j = get_node(network, vals[2])
            p.endnode = j
        if len(vals) > 3:
            p.length = float(vals[3])
        if len(vals) > 4:
            p.diameter = float(vals[4])
        if len(vals) > 5:
            p.roughness = float(vals[5])
        if len(vals) > 6:
            p.minorloss = float(vals[6])
        if len(vals) > 7:
            p.status = vals[7].upper()

        network.pipes.append(p)


@section_reader('PUMPS', 2)
def read_pumps(network, block):
    for vals in block:
        comment = vals['comments'][0] if vals['comments'] else None
        vals = vals['values']
        p = Pump(id=vals[0], comment=comment, tag=None)
        if len(vals) > 1:
            j = get_node(network, vals[1])
            p.startnode = j
        if len(vals) > 2:
            j = get_node(network, vals[2])
            p.endnode = j
        if len(vals) > 3:
            p.keyword = vals[3]
        if len(vals) > 4:
            p.value = " ".join(vals[4:])
        network.pumps.append(p)


@section_reader('VALVES', 2)
def read_valves(network, block):
    for vals in block:
        comment = vals['comments'][0] if vals['comments'] else None
        vals = vals['values']
        if vals[4] == 'PRV':
            v = PRV(id=vals[0], comment=comment, tag=None)
        elif vals[4] == 'TCV':
            v = TCV(id=vals[0], comment=comment, tag=None)
        elif vals[4] == 'PSV':
            v = PSV(id=vals[0], comment=comment, tag=None)
        elif vals[4] == 'GPV':
            v = GPV(id=vals[0], comment=comment, tag=None)
        elif vals[4] == 'PBV':
            v = PBV(id=vals[0], comment=comment, tag=None)
        elif vals[4] == 'FCV':
            v = FCV(id=vals[0], comment=comment, tag=None)
        else:
            v = Valve(id=vals[0], comment=comment, tag=None)
        if len(vals) > 1:
            j = get_node(network, vals[1])
            v.startnode = j
        if len(vals) > 2:
            j = get_node(network, vals[2])
            v.endnode = j
        if len(vals) > 3:
            v.diameter = float(vals[3])
        if len(vals) > 4:
            v.valvetype = vals[4]
        if len(vals) > 5:
            v.setting = vals[5]
        if len(vals) > 6:
            v.minorloss = float(vals[6])
        network.valves.append(v)


@section_reader('EMITTERS', 2)
def read_emitters(network, block):
    for vals in block:
        vals = vals['values']
        j = get_junction(network, vals[0])
        j.emittercoefficient = float(vals[1])

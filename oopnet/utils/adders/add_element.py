from ...elements.network_components import *


def add_pattern(network, pattern):
    if network.patterns:
        network.patterns.append(pattern)
    else:
        network.patterns = [pattern]


def add_junction(network, id, xcoordinate=0.0, ycoordinate=0.0, elevation=0.0, initialquality=0.0,
                sourcequality=0.0, sourcetype=None, strength=0.0, sourcepattern=None, emittercoefficient=0.0,
                demandpattern=None, demand=None, comment=None):
    '''
    This function adds a Junction to an OOPNET network.

    :param network: OOPNET network object
    :param id: ID of the Junction
    '''
    j = None
    if network.junctions:
        try:
            j = network.networkhash['node'][id]
        except:
            pass
    if not j:
        if comment:
            j = Junction(id=id, comment=comment)
        else:
            j = Junction(id=id)
    if xcoordinate:
        j.xcoordinate = xcoordinate
    if ycoordinate:
        j.ycoordinate = ycoordinate
    if elevation:
        j.elevation = elevation
    if initialquality:
        j.initialquality = initialquality
    if sourcequality:
        j.sourcequality = sourcequality
    if sourcetype:
        j.sourcetype = sourcetype
    if strength:
        j.strength = strength
    if sourcepattern:
        j.sourcepattern = sourcepattern
    if emittercoefficient:
        j.emittercoefficient = emittercoefficient
    if demandpattern:
        j.demandpattern = demandpattern
    if demand:
        j.demand = demand

    if network.junctions is None:
        network.junctions = [j]
    else:
        network.junctions.append(j)
    network.networkhash['node'][id] = j


def add_reservoir(network, id, xcoordinate=0.0, ycoordinate=0.0, elevation=0.0, initialquality=0.0,
                 sourcequality=0.0, sourcetype=None, strength=0.0, sourcepattern=None, head=1.0, headpattern=None,
                 mixingmodel=None, comment=None):
    '''
    This function adds a Reservoir to an OOPNET network.

    :param network: OOPNET network object
    :param id: ID of the Reservoir
    '''
    r = None
    if network.reservoirs:
        try:
            r = network.networkhash['node'][id]
        except:
            pass
    if not r:
        if comment:
            r = Reservoir(id=id, comment=comment)
        else:
            r = Reservoir(id=id)
    if xcoordinate:
        r.xcoordinate = xcoordinate
    if ycoordinate:
        r.ycoordinate = ycoordinate
    if elevation:
        r.elevation = elevation
    if initialquality:
        r.initialquality = initialquality
    if sourcequality:
        r.sourcequality = sourcequality
    if sourcetype:
        r.sourcetype = sourcetype
    if strength:
        r.strength = strength
    if sourcepattern:
        r.sourcepattern = sourcepattern
    if head:
        r.head = head
    if headpattern:
        r.headpattern = headpattern
    if mixingmodel:
        r.mixingmodel = mixingmodel

    if network.reservoirs is None:
        network.reservoirs = [r]
    else:
        network.reservoirs.append(r)
    network.networkhash['node'][id] = r


def add_tank(network, id, xcoordinate=0.0, ycoordinate=0.0, elevation=0.0, initialquality=0.0,
            sourcequality=0.0, sourcetype=None, strength=0.0, sourcepattern=None, compartmentvolume=0.0,
            initlevel=0.5, maxlevel=1.0, minlevel=0.0, minvolume=0.0, mixingmodel=None, reactiontank=0.0,
            volumecurve=None, comment=None):
    '''
    This function adds a Tank to an OOPNET network.

    :param network: OOPNET network object
    :param id: ID of the tank
    '''
    t = None
    if network.tanks:
        try:
            t = network.networkhash['node'][id]
        except:
            pass
    if not t:
        if comment:
            t = Tank(id=id, comment=comment)
        else:
            t = Tank(id=id)
    if xcoordinate:
        t.xcoordinate = xcoordinate
    if ycoordinate:
        t.ycoordinate = ycoordinate
    if elevation:
        t.elevation = elevation
    if initialquality:
        t.initialquality = initialquality
    if sourcequality:
        t.sourcequality = sourcequality
    if sourcetype:
        t.sourcetype = sourcetype
    if strength:
        t.strength = strength
    if sourcepattern:
        t.sourcepattern = sourcepattern
    if compartmentvolume:
        t.compartmentvolume = compartmentvolume
    if initlevel:
        t.initlevel = initlevel
    if maxlevel:
        t.maxlevel = maxlevel
    if minlevel:
        t.minlevel = minlevel
    if minvolume:
        t.minvolume = minvolume
    if mixingmodel:
        t.mixingmodel = mixingmodel
    if reactiontank:
        t.reactiontank = reactiontank
    if volumecurve:
        t.volumecurve = volumecurve

    if network.tanks is None:
        network.tanks = [t]
    else:
        network.tanks.append(t)
    network.networkhash['node'][id] = t


def add_pipe(network, id, startnode, endnode, diameter=100.0, length=100.0, roughness=0.1,
             minorloss=0.0, reactionbulk=0.0, reactionwall=0.0, comment=None, tag=None, status=None):
    '''
    This function adds a Pipe to an OOPNET network.

    :param network: OOPNET network object
    :param id: ID of the Pipe
    '''
    p = None
    if network.pipes:
        try:
            p = network.networkhash['link'][id]
        except:
            pass
    if not p:
        if comment:
            p = Pipe(id=id, comment=comment)
        else:
            p = Pipe(id=id)
    p.startnode = startnode
    p.endnode = endnode

    if tag:
        p.tag = tag
    if diameter:
        p.diameter = diameter
    if length:
        p.length = length
    if minorloss:
        p.minorloss = minorloss
    if reactionbulk:
        p.reactionbulk = reactionbulk
    if reactionwall:
        p.reactionwall = reactionwall
    if roughness:
        p.roughness = roughness
    if status:
        p.status = status

    if network.pipes is None:
        network.pipes = [p]
    else:
        network.pipes.append(p)
    network.networkhash['link'][id] = p


def add_pump(network, id, keyword, value, startnode, endnode, comment=None, tag=None):
    '''
    This function adds a Pump to an OOPNET network.

    :param network: OOPNET network object
    :param id: ID of the Pump
    '''
    p = None
    if network.pumps:
        try:
            p = network.networkhash['link'][id]
        except:
            pass
    if not p:
        if comment:
            p = Pump(id=id, comment=comment)
        else:
            p = Pump(id=id)
    p.startnode = startnode
    p.endnode = endnode
    p.keyword = keyword
    p.value = value

    if tag:
        p.tag = tag

    if network.pumps is None:
        network.pumps = [p]
    else:
        network.pumps.append(p)
    network.networkhash['link'][id] = p


def add_valve(network, id, startnode, endnode, valvetype, diameter=100.0, minorloss=0.0, comment=None, tag=None):
    '''
    This function adds a Valve to an OOPNET network.

    :param network: OOPNET network object
    :param id: ID of the Valve
    '''
    v = None
    if network.valves:
        try:
            v = network.networkhash['link'][id]
        except:
            pass
    if not v:
        if comment:
            v = Valve(id=id, comment=comment)
        else:
            v = Valve(id=id)
    v.startnode = startnode
    v.endnode = endnode
    v.valvetype = valvetype

    if tag:
        v.tag = tag
    if diameter:
        v.diameter = diameter
    if minorloss:
        v.minorloss = minorloss

    if network.valves is None:
        network.valves = [v]
    else:
        network.valves.append(v)
    network.networkhash['link'][id] = v

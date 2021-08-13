from .decorators import section_writer


@section_writer('QUALITY', 3)
def write_quality(network, fid):
    print('[QUALITY]', file=fid)
    print(';id initialquality', file=fid)
    for key in network.networkhash['node']:
        n = network.networkhash['node'][key]
        if n.initialquality > 0.0:
            print(n.id, n.initialquality, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('REACTIONS', 3)
def write_reactions(network, fid):
    print('[REACTIONS]', file=fid)
    if network.reactions is not None:
        r = network.reactions
        if r.orderbulk is not None:
            print('ORDER BULK', r.orderbulk, file=fid)
        if r.orderwall is not None:
            print('ORDER WALL', r.orderwall, file=fid)
        if r.ordertank is not None:
            print('ORDER TANK', r.ordertank, file=fid)
        if r.globalbulk is not None:
            print('GLOBAL BULK', r.globalbulk, file=fid)
        if r.globalwall is not None:
            print('GLOBAL WALL', r.globalwall, file=fid)
        if r.limitingpotential is not None:
            print('LIMITING POTENTIAL', r.limitingpotential, file=fid)
        if r.roughnesscorrelation is not None:
            print('ROUGHNESS CORRELATION', r.roughnesscorrelation, file=fid)
        if r.bulk is not None:
            for p in r.bulk:
                print('BULK', p.id, p.reactionbulk, file=fid)
        if r.wall is not None:
            for p in r.wall:
                print('WALL', p.id, p.reactionwall, file=fid)
        if r.tank is not None:
            for p in r.tank:
                print('TANK', p.id, p.tank, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('SOURCES', 3)
def write_sources(network, fid):
    print('[SOURCES]', file=fid)
    print(';id sourcetype strength sourcepattern', file=fid)
    for key in network.networkhash['node']:
        n = network.networkhash['node'][key]
        if n.sourcetype is not None:
            print(n.id, n.sourcetype, end=' ', file=fid)
            if n.strength > 0.0:
                print(n.strength, end=' ', file=fid)
            if n.sourcepattern is not None:
                print(n.sourcepattern.id, end=' ', file=fid)
            print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('MIXING', 3)
def write_mixing(network, fid):
    print('[MIXING]', file=fid)
    print(';tankid mixingmodel compartmentvolume', file=fid)
    if network.tanks is not None:
        for t in network.tanks:
            if t.mixingmodel is not None:
                print(t.id, t.mixingmodel, end=' ', file=fid)
                if t.compartmentvolume != 0.0:
                    print(t.compartmentvolume, end=' ', file=fid)
                print('\n', end=' ', file=fid)
    print('\n', end=' ', file=fid)

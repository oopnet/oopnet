from .decorators import section_writer


@section_writer('COORDINATES', 4)
def write_coordinates(network, fid):
    print('[COORDINATES]', file=fid)
    print(';nodeid xcoordinate ycoordinate', file=fid)
    for key in sorted(network.networkhash['node'].keys()):
        n = network.networkhash['node'][key]
        print(n.id, n.xcoordinate, n.ycoordinate, file=fid)
    print('\n', end=' ', file=fid)


@section_writer('VERTICES', 4)
def write_vertices(network, fid):
    # ToDo: Implement Printer for Vertices
    print('[VERTICES]', file=fid)
    print(';linkkid xcoordinate ycoordinate', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('LABELS', 4)
def write_labels(network, fid):
    # ToDo: Implement Printer for Labels
    print('[LABELS]', file=fid)
    print(';xcoordinate ycoordinate label anchornode', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('BACKDROP', 4)
def write_backdrop(network, fid):
    # ToDo: Implement Printer for Backdrop
    print('[BACKDROP]', file=fid)
    print('\n', end=' ', file=fid)


@section_writer('TAGS', 4)
def write_tags(network, fid):
    # ToDo: Implement Printer for Tags
    print('[TAGS]', file=fid)
    print('\n', end=' ', file=fid)

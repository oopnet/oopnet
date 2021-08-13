from .decorators import section_reader


@section_reader('COORDINATES', 4)
def read_coordinates(network, block):
    for vals in block:
        vals = vals['values']
        j = network.networkhash['node'][vals[0]]
        if len(vals) > 1:
            j.xcoordinate = float(vals[1])
        if len(vals) > 2:
            j.ycoordinate = float(vals[2])


@section_reader('VERTICES', 4)
# ToDo: Implement Vertices Reader
def read_vertices(network, block):
    pass


@section_reader('LABELS', 4)
# ToDo: Implement Labelreader
def read_labels(network, block):
    pass


@section_reader('BACKDROP', 4)
# ToDo: Implement Backdrop Reader
def read_backdrop(network, block):
    pass


@section_reader('TAGS', 4)
# ToDo: Implement Tagreader
def read_tags(network, block):
    pass

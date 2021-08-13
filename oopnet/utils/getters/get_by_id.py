# Retrieve a specific instance of an object contained in the network with a specific id
def get_junction(network, id):
    """
    This function returns a specific Junction from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Junction
    :return: Junction with property id
    """
    return next(filter(lambda x: x.id == id, network.junctions))


def get_tank(network, id):
    """
    This function returns a specific Tank from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Tank
    :return: Tank with property id
    """
    return next(filter(lambda x: x.id == id, network.tanks))


def get_reservoir(network, id):
    """
    This function returns a specific Reservoir from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Resercvoir
    :return: Reservoir with property id
    """
    return next(filter(lambda x: x.id == id, network.reservoirs))


def get_pipe(network, id):
    """
    This function returns a specific Pipe from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Pipe
    :return: Pipe with property id
    """
    return next(filter(lambda x: x.id == id, network.pipes))


def get_pump(network, id):
    """
    This function returns a specific Pump from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Pump
    :return: Pump with property id
    """
    return next(filter(lambda x: x.id == id, network.pumps))


def get_valve(network, id):
    """
    This function returns a specific Valve from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Valve
    :return: Valve with property id
    """
    return next(filter(lambda x: x.id == id, network.valves))


def get_curve(network, id):
    """
    This function returns a specific Curve from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Curve
    :return: Curve with property id
    """
    return next(filter(lambda x: x.id == id, network.curves))


def get_pattern(network, id):
    """
    This function returns a specific Pattern from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Pattern
    :return: Pattern with property id
    """
    return next(filter(lambda x: x.id == id, network.patterns))


def get_rule(network, id):
    """
    This function returns a specific Rule from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Rule
    :return: Rule with property id
    """
    return next(filter(lambda x: x.id == id, network.rules))


def get_node(network, id):
    """
    This function returns a specific Node from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Node
    :return: Node with property id
    """
    result = None
    if network.junctions:
        if id in [x.id for x in network.junctions]:
            result = get_junction(network, id)
    if network.tanks:
        if not result:
            if id in [x.id for x in network.tanks]:
                result = get_tank(network, id)
    if network.reservoirs:
        if not result:
            if id in [x.id for x in network.reservoirs]:
                result = get_reservoir(network, id)
    return result


def get_link(network, id):
    """
    This function returns a specific Link from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Link
    :return: Link with property id
    """
    result = None
    if network.pipes:
        if id in [x.id for x in network.pipes]:
            result = get_pipe(network, id)
    if network.pumps:
        if not result:
            if id in [x.id for x in network.pumps]:
                result = get_pump(network, id)
    if network.valves:
        if not result:
            if id in [x.id for x in network.valves]:
                result = get_valve(network, id)
    return result

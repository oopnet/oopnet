# Retrieve a specific instance of an object contained in the network with a specific id


def get_junction(network, id):
    """
    This function returns a specific Junction from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Junction
    :return: Junction with property id
    """
    return network.junctions.binary_search(id)


def get_tank(network, id):
    """
    This function returns a specific Tank from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Tank
    :return: Tank with property id
    """
    return network.tanks.binary_search(id)


def get_reservoir(network, id):
    """
    This function returns a specific Reservoir from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Reservoir
    :return: Reservoir with property id
    """
    return network.reservoirs.binary_search(id)


def get_pipe(network, id):
    """
    This function returns a specific Pipe from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Pipe
    :return: Pipe with property id
    """
    return network.pipes.binary_search(id)


def get_pump(network, id):
    """
    This function returns a specific Pump from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Pump
    :return: Pump with property id
    """
    return network.pumps.binary_search(id)


def get_valve(network, id):
    """
    This function returns a specific Valve from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Valve
    :return: Valve with property id
    """
    return network.valves.binary_search(id)


def get_curve(network, id):
    """
    This function returns a specific Curve from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Curve
    :return: Curve with property id
    """
    return network.curves.binary_search(id)


def get_pattern(network, id):
    """
    This function returns a specific Pattern from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Pattern
    :return: Pattern with property id
    """
    return network.patterns.binary_search(id)


def get_rule(network, id):
    """
    This function returns a specific Rule from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Rule
    :return: Rule with property id
    """
    return network.rules.binary_search(id)


def get_node(network, id):
    """
    This function returns a specific Node from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Node
    :return: Node with property id
    """
    return network.nodes.binary_search(id)


def get_link(network, id):
    """
    This function returns a specific Link from the network with a specific id

    :param network: OOPNET network object
    :param id: id of the Link
    :return: Link with property id
    """
    return network.links.binary_search(id)

# Retrieve all id's of specific objects
def get_junction_ids(network):
    """
    Function for getting all junction ids in a network

    :param network: OOPNET network object
    :return: list of junction ids
    """
    ids = []
    if network.junctions:
        ids = [x.id for x in network.junctions]
    return ids


def get_tank_ids(network):
    """
    Function for getting all tank ids in a network

    :param network: OOPNET network object
    :return: list of tank ids
    """
    ids = []
    if network.tanks:
        ids = [x.id for x in network.tanks]
    return ids


def get_reservoir_ids(network):
    """
    Function for getting all reservoir ids in a network

    :param network: OOPNET network object
    :return: list of reservoir ids
    """
    ids = []
    if network.reservoirs:
        ids = [x.id for x in network.reservoirs]
    return ids


def get_node_ids(network):
    """
    Function for getting all node ids in a network

    :param network: OOPNET network object
    :return: list of node ids
    """
    return get_junction_ids(network) + get_tank_ids(network) + get_reservoir_ids(network)


def get_pipe_ids(network):
    """
    Function for getting all pipe ids in a network

    :param network: OOPNET network object
    :return: list of pipe ids
    """
    ids = []
    if network.pipes:
        ids = [x.id for x in network.pipes]
    return ids


def get_pump_ids(network):
    """
    Function for getting all pump ids in a network

    :param network: OOPNET network object
    :return: list of pump ids
    """
    ids = []
    if network.pumps:
        ids = [x.id for x in network.pumps]
    return ids


def get_valve_ids(network):
    """
    Function for getting all valve ids in a network

    :param network: OOPNET network object
    :return: list of valve ids
    """
    ids = []
    if network.valves:
        ids = [x.id for x in network.valves]
    return ids


def get_link_ids(network):
    """
    Function for getting all link ids in a network

    :param network: OOPNET network object
    :return: list of link ids
    """
    return get_pipe_ids(network) + get_pump_ids(network) + get_valve_ids(network)

# Retrieve all specific objects
def get_pipes(network):
    """
    This function returns all network pipes as a list

    :param network: OOPNET network object
    :return: list of pipes
    """
    objects = []
    if network.pipes:
        objects = network.pipes
    return objects


def get_junctions(network):
    """
    This function returns all network junctions as a list

    :param network: OOPNET network object
    :return: list of junctions
    """
    objects = []
    if network.junctions:
        objects = network.junctions
    return objects


def get_reservoirs(network):
    """
    This function returns all reservoirs in the network as a list

    :param network: OOPNET network object
    :return: list of reservoirs
    """
    objects = []
    if network.reservoirs:
        objects = network.reservoirs
    return objects


def get_tanks(network):
    """
    This function returns all tanks in the network as a list

    :param network: OOPNET network object
    :return: list of tanks
    """
    objects = []
    if network.tanks:
        objects = network.tanks
    return objects


def get_nodes(network):
    """
    This function returns all network nodes as a list (junctions, tanks and reservoirs)

    :param network: OOPNET network object
    :return: list of nodes
    """
    objects = []
    if network.junctions:
        objects += network.junctions
    if network.tanks:
        objects += network.tanks
    if network.reservoirs:
        objects += network.reservoirs
    return objects


def get_links(network):
    """
    This function returns all network links as a list (pipes, pumps and valves)

    :param network: OOPNET network object
    :return: list of links
    """
    objects = []
    if network.pipes:
        objects += network.pipes
    if network.pumps:
        objects += network.pumps
    if network.valves:
        objects += network.valves
    return objects

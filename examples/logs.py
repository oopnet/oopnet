import os
import logging

import oopnet as on

logger = on.start_logger()

filename = os.path.join('data', 'Poulakis.inp')

net = on.Network.read(filename)

logger.setLevel(logging.DEBUG)

net = on.Network.read(filename)

logger = logging.getLogger('oopnet')


@on.logging_decorator(logger)
def do_some_crazy_things():
    a = 0
    for b in [0, 1, 2, 'a']:
        a += b
    return a


do_some_crazy_things()

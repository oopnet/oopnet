import os
import logging

from oopnet import *

logger = start_logger()

filename = os.path.join('data', 'Poulakis.inp')

net = Read(filename)

logger.setLevel(logging.DEBUG)

net = Read(filename)

logger = logging.getLogger('oopnet')


@logging_decorator(logger)
def do_some_crazy_things():
    a = 0
    for b in [0, 1, 2, 'a']:
        a += b
    return a


do_some_crazy_things()

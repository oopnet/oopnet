from typing import Callable, Optional
from dataclasses import dataclass


@dataclass
class ReaderDecorator:
    """
    Class for saving the reader function properties in a proper way with the decorators
    """

    sectionname: Optional[str] = None
    functionname: Optional[str] = None
    priority: Optional[int] = None
    readerfunction: Optional[Callable] = None


def make_registering_decorator_factory(foreign_decorator_factory):

    def new_decorator_factory(*args, **kw):
        old_generated_decorator = foreign_decorator_factory(*args, **kw)

        def new_generated_decorator(func):
            modified_func = old_generated_decorator(func)
            modified_func.decorator = new_decorator_factory  # keep track of decorator
            modified_func.decorator_args = args
            modified_func.decorator_kwargs = kw
            return modified_func
        return new_generated_decorator
    new_decorator_factory.__name__ = foreign_decorator_factory.__name__
    new_decorator_factory.__doc__ = foreign_decorator_factory.__doc__
    return new_decorator_factory


def section_reader(title, priority):
    """ Synchronization decorator """
    def wrap(f):
        def new_function(*args, **kw):
            # print "From decorator"
            return f(*args, **kw)
        return new_function
    return wrap

section_reader = make_registering_decorator_factory(section_reader)

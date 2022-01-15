from typing import Callable, Type

import inspect

from oopnet.reader.decorators import section_reader, ReaderDecorator


def pred(c: Type[Callable]) -> bool:
    """Checks if a class or function is decorated with section_reader.

    Args:
      c: callable to be checked

    Returns:
        Returns True if the class or function is decorated with section_reader and False otherwise.
    """
    return hasattr(c, 'decorator') and c.decorator == section_reader


def list_section_reader_callables(modules) -> list[Type[Callable]]:
    """Lists all callables decorated with the section_reader decorator from a list of modules.

    Args:
      modules: list of modules to be checked for callables decorated with section_reader.

    Returns:
        List of callables decorated with section_reader.
    """

    all_functions = []
    for module in modules:
        funcs = inspect.getmembers(module, pred)
        for f in funcs:
            r = ReaderDecorator(sectionname=f[1].decorator_args[0],
                                functionname=f[0],
                                priority=f[1].decorator_args[1],
                                readerfunction=f[1])
            all_functions.append(r)
    return all_functions

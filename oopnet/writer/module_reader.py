from typing import Type, Callable

import inspect

from oopnet.writer.decorators import section_writer, WriterDecorator


def pred(c: Type[Callable]) -> bool:
    """Checks if a class or function is decorated with section_writer.

    Args:
      c: callable to be checked

    Returns:
        Returns True if the class or function is decorated with section_writer and False otherwise.
    """
    return inspect.isfunction(c) and hasattr(c, 'decorator') and c.decorator == section_writer


def list_section_writer_callables(modules):
    """Lists all callables decorated with the section_writer decorator from a list of modules.

    Args:
      modules: list of modules to be checked for callables decorated with section_writer.

    Returns:
        List of callables decorated with section_writer.
    """

    all_functions = []
    for module in modules:
        funcs = inspect.getmembers(module, pred)
        for f in funcs:
            r = WriterDecorator(sectionname=f[1].decorator_args[0],
                                functionname=f[0],
                                priority=f[1].decorator_args[1],
                                writerfunction=f[1])
            all_functions.append(r)
    return all_functions

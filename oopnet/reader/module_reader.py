import inspect

from oopnet.reader.decorators import section_reader, ReaderDecorator


def pred(c):
    """

    Args:
      c: 

    Returns:

    """

    return inspect.isfunction(c) and hasattr(c, 'decorator') and c.decorator == section_reader


def list_all_functions_with_decorator(modules, decorator):
    """

    Args:
      modules: 
      decorator: 

    Returns:

    """

    all_functions = list()
    for module in modules:
        funcs = inspect.getmembers(module, pred)
        for f in funcs:
            r = ReaderDecorator(sectionname=f[1].decorator_args[0],
                                functionname=f[0],
                                priority=f[1].decorator_args[1],
                                readerfunction=f[1])
            all_functions.append(r)
    return all_functions

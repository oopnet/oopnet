from typing import Optional, Callable


class WriterDecorator:
    """Class for saving the writer function properties in a proper way with the decorators

    Attributes:
        sectionname:
        functionname:
        priority:
        writerfunction:

    """
    # todo: do None defaults make sense here?
    def __init__(self, sectionname: Optional[str] = None, functionname: Optional[str] = None,
                 priority: Optional[int] = None, writerfunction: Optional[Callable] = None):
        self.sectionname = sectionname
        self.functionname = functionname
        self.priority = priority
        self.writerfunction = writerfunction


def make_registering_decorator_factory(foreign_decorator_factory):
    """

    Args:
      foreign_decorator_factory: 

    Returns:

    """

    def new_decorator_factory(*args, **kw):
        """

        Args:
          *args: 
          **kw: 

        Returns:

        """
        old_generated_decorator = foreign_decorator_factory(*args, **kw)

        def new_generated_decorator(func):
            """

            Args:
              func: 

            Returns:

            """
            modified_func = old_generated_decorator(func)
            modified_func.decorator = new_decorator_factory  # keep track of decorator
            modified_func.decorator_args = args
            modified_func.decorator_kwargs = kw
            return modified_func

        return new_generated_decorator

    new_decorator_factory.__name__ = foreign_decorator_factory.__name__
    new_decorator_factory.__doc__ = foreign_decorator_factory.__doc__
    return new_decorator_factory


def section_writer(title: str, priority: int):
    """Synchronization decorator

    Args:
      title: section title
      priority: write priority

    Returns:

    """

    def wrap(f):
        """

        Args:
          f: 

        Returns:

        """

        def new_function(*args, **kw):
            """

            Args:
              *args: 
              **kw: 

            Returns:

            """
            return f(*args, **kw)

        return new_function

    return wrap

section_writer = make_registering_decorator_factory(section_writer)

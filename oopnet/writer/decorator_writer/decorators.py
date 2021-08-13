from traits.api import HasStrictTraits, Str, Function, Int


class WriterDecorator(HasStrictTraits):
    """
    Class for saving the writer function properties in a proper way with the decorators
    """

    __sectionname = Str
    __functionname = Str
    __priority = Int
    __writerfunction = Function

    @property
    def sectionname(self):
        return self.__sectionname

    @sectionname.setter
    def sectionname(self, value):
        self.__sectionname = value

    @property
    def functionname(self):
        return self.__functionname

    @functionname.setter
    def functionname(self, value):
        self.__functionname = value

    @property
    def priority(self):
        return self.__priority

    @priority.setter
    def priority(self, value):
        self.__priority = value

    @property
    def writerfunction(self):
        return self.__writerfunction

    @writerfunction.setter
    def writerfunction(self, value):
        self.__writerfunction = value

    def __init__(self, sectionname=None, functionname=None, priority=None, writerfunction=None):
        super(WriterDecorator, self).__init__()
        if sectionname is not None:
            self.__sectionname = sectionname
        if functionname is not None:
            self.__functionname = functionname
        if priority is not None:
            self.__priority = priority
        if writerfunction is not None:
            self.__writerfunction = writerfunction


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


def section_writer(title, priority):
    """ Synchronization decorator """

    def wrap(f):

        def new_function(*args, **kw):
            # print "From decorator"
            return f(*args, **kw)

        return new_function

    return wrap

section_writer = make_registering_decorator_factory(section_writer)

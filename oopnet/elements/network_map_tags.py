from traits.api import HasStrictTraits, Float, Str, ListFloat, Enum
from .base import NetworkComponent
from .network_components import Node


class Vertex(HasStrictTraits):
    # ToDo: Implement Vertex
    """
    .. warning::
        Not implemented yet
    """
    pass


class Label(HasStrictTraits):
    """
    Assigns coordinates to map labels.
    """

    __xcoordinate = Float
    __ycoordinate = Float
    __label = Str
    __anchor = Node

    @property
    def xcoordinate(self):
        return self.__xcoordinate

    @xcoordinate.setter
    def xcoordinate(self, value):
        self.__xcoordinate = value

    @property
    def ycoordinate(self):
        return self.__ycoordinate

    @ycoordinate.setter
    def ycoordinate(self, value):
        self.__ycoordinate = value

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    @property
    def anchor(self):
        return self.__anchor

    @anchor.setter
    def anchor(self, value):
        self.__anchor = value


class Backdrop(HasStrictTraits):
    """
    Identifies a backdrop image and dimensions for the network map.
    """

    __dimensions = ListFloat
    __units = Str
    __file = Str
    __offset = ListFloat

    @property
    def dimensions(self):
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, value):
        self.__dimensions = value

    @property
    def units(self):
        return self.__units

    @units.setter
    def units(self, value):
        self.__units = value

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, value):
        self.__file = value

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, value):
        self.__offset = value


class Tag(NetworkComponent):
    """
    Associates category labels (tags) with specific nodes and links.
    """

    __object = Enum('NODE', 'LINK')
    __tag = Str

    @property
    def object(self):
        return self.__object

    @object.setter
    def object(self, value):
        self.__object = value

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, value):
        self.__tag = value

from traits.api import HasStrictTraits, Float, Either, Instance, List
from ..elements.network_components import Pipe


class Reaction(HasStrictTraits):
    """Defines parameters related to chemical reactions occuring in the network."""
    __orderbulk = Float
    __orderwall = Float
    __ordertank = Float
    __globalbulk = Float
    __globalwall = Float
    __bulk = Either(Instance(Pipe), List(Instance(Pipe)))
    __wall = Either(Instance(Pipe), List(Instance(Pipe)))
    __tank = Either(Instance(Pipe), List(Instance(Pipe)))
    __limitingpotential = Float
    __roughnesscorrelation = Float

    @property
    def orderbulk(self):
        return self.__orderbulk

    @orderbulk.setter
    def orderbulk(self, value):
        self.__orderbulk = value

    @property
    def orderwall(self):
        return self.__orderwall

    @orderwall.setter
    def orderwall(self, value):
        self.__orderwall = value

    @property
    def ordertank(self):
        return self.__ordertank

    @ordertank.setter
    def ordertank(self, value):
        self.__ordertank = value

    @property
    def globalbulk(self):
        return self.__globalbulk

    @globalbulk.setter
    def globalbulk(self, value):
        self.__globalbulk = value

    @property
    def globalwall(self):
        return self.__globalwall

    @globalwall.setter
    def globalwall(self, value):
        self.__globalwall = value

    @property
    def bulk(self):
        return self.__bulk

    @bulk.setter
    def bulk(self, value):
        self.__bulk = value

    @property
    def wall(self):
        return self.__wall

    @wall.setter
    def wall(self, value):
        self.__wall = value

    @property
    def tank(self):
        return self.__tank

    @tank.setter
    def tank(self, value):
        self.__tank = value

    @property
    def limitingpotential(self):
        return self.__limitingpotential

    @limitingpotential.setter
    def limitingpotential(self, value):
        self.__limitingpotential = value

    @property
    def roughnesscorrelation(self):
        return self.__roughnesscorrelation

    @roughnesscorrelation.setter
    def roughnesscorrelation(self, value):
        self.__roughnesscorrelation = value

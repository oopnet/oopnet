from abc import abstractmethod
from typing import List, Type
from sys import modules
from inspect import getmembers, isclass


class EPANETSimulationError(Exception):
    def __init__(self, message):
        super().__init__(message)


# todo: implement as exceptions? (prevents raising multiple simulation errors)
class EPANETError:
    description = None

    @property
    @abstractmethod
    def code(self):
        """Error code as described in the EPANET manual."""

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        out = f'{self.__class__.__name__} | Error {self.code}: {self.message}'
        if self.description:
            out += f' {self.description}'
        return out

class InsufficientMemoryError(EPANETError):
    code = 101


class HydraulicEquationError(EPANETError):
    code = 110


class InputDataError(EPANETError):
    code = 200


class EPANETSyntaxError(EPANETError):
    code = 201


class IllegalNumericalValueError(EPANETError):
    code = 202


class UndefinedNodeError(EPANETError):
    code = 203


class UndefinedLinkError(EPANETError):
    code = 204


class UndefinedTimePatternError(EPANETError):
    code = 205


class UndefinedCurveError(EPANETError):
    code = 206


class CheckValveImmutableError(EPANETError):
    code = 207


class NodeReferenceError(EPANETError):
    code = 208


class IllegalNodePropertyError(EPANETError):
    code = 209


class LinkReferenceError(EPANETError):
    code = 210


class IllegalLinkPropertyError(EPANETError):
    code = 211


class UndefinedTraceNodeError(EPANETError):
    code = 212


class IllegalAnalysisOptionError(EPANETError):
    code = 213


class TooManyCharactersError(EPANETError):
    code = 214


class SharedIDError(EPANETError):
    code = 215


class UndefinedPumpError(EPANETError):
    code = 216


class InvalidEnergyDataError(EPANETError):
    code = 217


class IllegalValveSourceConnectionError(EPANETError):
    code = 219


class IllegalValveValveConnectionError(EPANETError):
    code = 220


class MisplacedRuleClause(EPANETError):
    code = 221


class NotEnoughNodesError(EPANETError):
    code = 223


class NotEnoughSourcesError(EPANETError):
    code = 224


class InvalidTankLevelError(EPANETError):
    code = 225


class InvalidPumpError(EPANETError):
    code = 227


class InvalidCurveError(EPANETError):
    code = 230


class UnconnectedNodeError(EPANETError):
    code = 233


class TempInputFileAccessError(EPANETError):
    code = 302


class ReportFileAccessError(EPANETError):
    code = 303


class BinaryOutputFileAccessError(EPANETError):
    code = 304


class ResultFileSavingError(EPANETError):
    code = 308


class ReportFileSavingError(EPANETError):
    code = 309


def get_error_list() -> List[Type[EPANETError]]:
    return [obj for name, obj in getmembers(modules[__name__]) if isclass(obj) and not issubclass(obj, EPANETSimulationError)]
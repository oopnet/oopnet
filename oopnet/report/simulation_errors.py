from abc import abstractmethod
from typing import Type, Union
from sys import modules
from inspect import getmembers, isclass


class EPANETError(Exception):
    """Base class for simulation errors.

    This exception is not meant to be called manually but is only a super class for the specific EPANET errors listed
    in the 'EPANET manual appendix concerning error messages
     <https://epanet22.readthedocs.io/en/latest/back_matter.html#error-messages>'.

    Attributes:
        code: error code as listed in the 'EPANET manual appendix concerning error messages
        <https://epanet22.readthedocs.io/en/latest/back_matter.html#error-messages>'

    """

    def __init__(self, description: str, details: str):
        """

        Args:
            description: general error message
            details: error details (if available)

        """
        msg = f'Error {self.code} - {description}'
        if details:
            msg += f' {details}'
        super().__init__(msg)

    @property
    @abstractmethod
    def code(self):
        """Error code as described in the EPANET manual."""


class EPANETSimulationError(Exception):
    """Error raised when any errors were encountered while simulating a hydraulic model."""

    def __init__(self, message):
        super().__init__(message)

    @property
    def errors(self):
        """Property containing all raised errors.

        This property can be used as a shortcut to the raised errors. Useful when looking for a specific kind of error.

        """
        return self.args[0]

    def _compare_instances(self, errorcls: Type[EPANETError]):
        return any(isinstance(x, errorcls) for x in self.errors)

    def check_contained_errors(self, errors: Union[Type[EPANETError], list[Type[EPANETError]]]):
        if isinstance(errors, list):
            return [self._compare_instances(error) for error in errors]
        return self._compare_instances(errors)


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


def get_error_list() -> list[Type[EPANETError]]:
    """Lists all errors implemented."""
    return [obj for name, obj in getmembers(modules[__name__]) if isclass(obj) and hasattr(obj, 'code')]

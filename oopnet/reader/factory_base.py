from abc import ABC


class LengthExceededError(Exception):
    """Exception for attribute lists that exceed their maximum specified length.

    Since there is a predefined number of attributes for every NetworkComponent subclass, a list of attributes read
    from an EPANET input file must not exceed this predefined length.

    """
    def __init__(self, actual_length, target_length):
        """
        Args:
            actual_length: actual number of elements in the list
            target_length: number of predefined attributes
        """
        msg = f'Maximum list length is {target_length} but the submitted list is of length {actual_length}.'
        super().__init__(msg)


class InvalidValveTypeError(Exception):
    """Exception for invalid Valve types read from an EPANET input file.

    A Valve can be one of six different types. This exception is raised, when an illegal Valve type is encountered in
    an EPANET input file.

    """
    def __init__(self, received):
        msg = f'An invalid Valve type {received} was passed.'
        super().__init__(msg)


class ReadFactory(ABC):
    """Abstract factory for EPANET input file reading."""
    @staticmethod
    def _pad_list(alist: list, target_length: int) -> list:
        """Extends a list to a certain length with None values.

        Raises:
            LengthExceededError is raised if the length of alist exceeds target_length.

        """
        length = len(alist)
        if length > target_length:
            raise LengthExceededError(actual_length=length, target_length=target_length)
        alist.extend([None] * (target_length - length))
        return alist

from abc import ABC


class LengthExceededError(Exception):
    def __init__(self, list_legnth, target_length):
        msg = f'Maximum list length is {target_length} but the submitted list is of length {list_legnth}.'
        super().__init__(msg)


class InvalidValveTypeError(Exception):
    def __init__(self, received):
        msg = f'An invalid Valve type {received} was passed.'
        super().__init__(msg)


class ReadFactory(ABC):
    @staticmethod
    def _pad_list(alist: list, target_length: int) -> list:
        length = len(alist)
        if length > target_length:
            raise LengthExceededError(list_legnth=length, target_length=target_length)
        alist.extend([None] * (target_length - length))
        return alist

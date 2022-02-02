import logging
from logging.handlers import RotatingFileHandler
from typing import Union
import functools


def start_logger(level: Union[int, str] = logging.INFO) -> logging.Logger:
    """Initializes a RotatingFileHanlder and a StreamHandler for logging.

    This function creates a logger with two handlers (RotatingFileHandler and StreamHandler) that can come in handy, if
    no other logging handlers are being used. The RotatingFileHandler writes it's output to 'oopnet.log' and rotates the
    file when it reaches a size of 5 MB.

    Args:
        level: logging level (e.g., logging.DEBUG)

    Returns:
        logger object

    """
    logger = logging.getLogger('oopnet')
    logger.setLevel(level)
    format = logging.Formatter('%(asctime)s:  %(name)s - %(levelname)s - %(message)s')
    f_handler = RotatingFileHandler('oopnet.log', maxBytes=5_000_000)
    f_handler.setFormatter(format)
    s_handler = logging.StreamHandler()
    s_handler.setFormatter(format)
    logger.addHandler(f_handler)
    logger.addHandler(logging.StreamHandler())
    return logger


def logging_decorator(logger: logging.Logger):
    """Decorates a function to log exceptions.

    Args:
        logger: logger to be used for logging

    Returns:
        decorated function
    """
    def decorate(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                logger.exception(f'Error raised by {func.__name__!r}')
                raise
        return wrapper
    return decorate

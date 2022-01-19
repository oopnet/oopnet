import time
import functools


def tic():
    """Start stopwatch timer."""
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    """Read elapsed time from stopwatch."""
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        raise Exception("Toc: start time not set")


def time_it(func):
    """Decorates a function to measure its execution time.

    Args:
        func: callable to time

    Returns:
        decorated function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_end = time.time()
        t_passed = t_end - t_start
        print(f'{func.__name__} took {t_passed} s to complete.')
        return result
    return wrapper

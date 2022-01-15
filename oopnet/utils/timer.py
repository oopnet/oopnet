import time


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

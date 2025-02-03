import math
import sys


def foo():
    try:
        import multiprocessing

        print(multiprocessing.cpu_count())
    except ImportError:
        print(sys.version)
    return math.pi

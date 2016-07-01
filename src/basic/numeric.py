import math
import numpy
import sys

def distance_numpy(array1, array2):
    """
    Get the distance between two points
    :param array1: numpy.Array
    :param array2: numpy.Array
    :rtype: float
    """

    return numpy.linalg.norm(array1-array2)


def distance(x1, y1, z1, x2, y2, z2):
    """
    Get the distance between variables.
    :param x1: float
    :param y1: float
    :param z1: float
    :param x2: float
    :param y2: float
    :param z2: float
    :rtype: float
    """

    return math.sqrt( math.pow( (x1-x2), 2) ) + math.sqrt( math.pow( (y1-y2), 2) )  + math.sqrt( math.pow( (z1-z2), 2) )

def get_perc(freq, total):
    """
    Get percent
    """
    freq = int(freq)
    total = float(total)

    if freq==0 and total==0:
        return 1000
    if total==0:
        sys.exit("cannot calculate percent as total is 0!")
    return freq/total *100


def get_s_perc(freq, total):
    """
    Get string of percent
    """
    return get_n_s(get_perc(freq, total))

def get_n_s(num):
    """
    Get a string for a float at .2f
    """
    if num == None:
        return 'None'
    return "%.2f"%num
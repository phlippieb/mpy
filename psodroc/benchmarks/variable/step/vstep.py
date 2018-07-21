import numpy as np


def function(xs, step_size):
    """Step function with variable step size.
    step_size defines the minimum distance to the next step.
    low = -20.
    high = 20.
    """
    return np.sum(np.square(np.floor(x/step_size + .5)*step_size) for x in xs)

# domain is [-20, 20] across all dimensions


def min(d):
    return -20.


def max(d):
    return 20.


def is_dimensionality_valid(D):
    return True

import numpy as np


def smallest(condition, min_e):
    # Find and return the smallest value that meets the given condition.
    # The result is accurate up to the exponential precision specified by min_e;
    # eg if min_e=-3, the precision is 0.001.

    # Find the smallest precision that overshoots the condition.
    e = 0
    while True:
        if condition(10 ** e):
            break
        e += 1

    # Keep track of a valid range:
    lower = 0.
    upper = 10. ** e

    # Search within the valid range at incrementally increasing precision.
    while e > min_e:
        e -= 1
        inc = 10. ** e

        for t in np.arange(lower, upper, inc):
            if condition(t):
                upper = t
                break
            else:
                lower = t

    return upper

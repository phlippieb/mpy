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
        range = upper - lower

        e -= 1
        inc = 10. ** e
        print '  find: lower={:.4f}, upper={:.4f}, inc={:.4f}'.format(
            lower, upper, inc)

        for t in np.arange(lower, upper, inc):
            if condition(t):
                upper = t
                break
            else:
                lower = t

    return upper


def smallest_2(condition, max_decimal_points):
    # Find the smallest precision that overshoots the condition.
    e = 0
    while True:
        if condition(10 ** e):
            break
        e += 1

    # Keep track of a valid range:
    lower = 0.
    upper = 10. ** e

    # binary search!
    while upper > lower:
        range = upper - lower
        mid = round(lower + (range / 2.), max_decimal_points)

        if condition(mid):
            if upper == mid:
                break
            upper = mid
        else:
            if lower == mid:
                break
            lower = mid

    return upper

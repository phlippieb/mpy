import numpy as np
from numba import vectorize

# S. K. Mishra. Some new test functions for global optimization and performance of repulsive particle swarm method. Technical Report 2718, University Library of Munich, Germany, August 2006.

def function(xs):
    D = len(xs)
    # return np.square(np.sin(3. * np.pi * xs[0])) \
    #     + np.sum(np.square(x1 - 1.) * (1. + np.square(np.sin(3. * np.pi * x2))) for x1, x2 in zip(xs[:-1], xs[1:])) \
    #     + np.square(xs[D-1] - 1.) * (1. + np.square(np.sin(2. * np.pi * xs[D-1])))

    return np.square(np.sin(3. * np.pi * xs[0])) \
        + np.sum(_inner(xs[:-1], xs[1:])) \
        + np.square(xs[D-1] - 1.) * (1. + np.square(np.sin(2. * np.pi * xs[D-1])))

@vectorize(['float64(float64, float64)'])
def _inner(x1, x2):
    return np.square(x1 - 1.) * (1. + np.square(np.sin(3. * np.pi * x2)))

# domain = [-10.0, 10.0] across all dimensions
def min(d):
    return -10.

def max(d):
    return 10.

def is_dimensionality_valid(D):
    return True

# Minimum is [1.0, ... 1.0] = 0.0

# Tests:
import pytest as pt

def _test_min():
    for D in [2, 5, 10, 20, 50]:
        m = np.full(D, 1.)
        assert function(m) == pt.approx(0., abs=1e-16)

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=2)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [2., 3.]
    assert function(xs) == 5.

    # TODO: add some higher-dimension tests.

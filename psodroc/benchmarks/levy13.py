import numpy as np

# S. K. Mishra. Some new test functions for global optimization and performance of repulsive particle swarm method. Technical Report 2718, University Library of Munich, Germany, August 2006.

def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("levy13.function is only defined for 2")
    x1 = xs[0]
    x2 = xs[1]

    return np.square(np.sin(3 * np.pi * x1)) \
        + np.square(x1 - 1.) * (1. + np.square(np.sin(3. * np.pi * x2))) \
        + np.square(x2 - 1.) * (1. + np.square(np.sin(2. * np.pi * x2)))

# domain = [-10.0, 10.0] across all dimensions
def min(d):
    return -10.

def max(d):
    return 10.

# Minimum is [1.0, ... 1.0] = 0.0

# Tests:
import pytest as pt

def _test_min():
    m = np.array([1., 1.])
    assert function(m) == pt.approx(0.)

    for i in range(100):
        p = np.random.uniform(low=min(0), high=max(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [2., 3.]
    assert function(xs) == 5.

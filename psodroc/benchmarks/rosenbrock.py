import numpy as np
from numba import vectorize

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    assert D > 1, "rosenbrock.function must have 2 or more dimensions."
    return np.sum(_inner(xs[:-1], xs[1:]))

@vectorize(['float64(float64, float64)'])
def _inner(xi, xi1):
    return (100. * np.square(xi1 - np.square(xi))) + np.square(xi - 1.)

# Domain is [-2.048, 2.048] across all dimensions
def min(d):
    return -2.048

def max(d):
    return 2.048

def is_dimensionality_valid(D):
    # Rosenbrock requires 2 or more dimensions.
    return D > 1

# Minimum is [1, ..., 1] = 0

# Tests:
import pytest as pt

def _test_min():
    for D in [2, 5, 10, 20, 50]:
        m = np.full(D, 1.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [1., 2., 3.]
    assert function(xs) == 201.
    xs = [3., 2., 1.]
    assert function(xs) == 5805.
    xs = [1., 2., 3., 4.]
    assert function(xs) == 2705.

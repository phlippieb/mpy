import numpy as np
from numba import vectorize

# K. A. De Jong. An analysis of the behavior of a class of genetic adaptive systems. PhD thesis, University of Michigan, Ann Arbor, MI, USA, 1975.

def function(xs):
    return np.sum(_inner(xs))

@vectorize(['float64(float64)'])
def _inner(x):
    return np.square(x)

# domain = [-5.12, 5.12] across all dimensions
def min(d):
    return -5.12

def max(d):
    return 5.12

def is_dimensionality_valid(D):
    return True

# min = [0.0, ... 0.0] = 0.0

# Tests:
import pytest as pt

def _test_min():
    for D in [2, 5, 10, 20, 50]:
        m = np.full(D, 0.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [1., 2., 3.]
    assert function(xs) == 14.

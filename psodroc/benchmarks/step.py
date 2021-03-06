import numpy as np
from numba import vectorize

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return np.sum(_inner(xs))

@vectorize(['float64(float64)'])
def _inner(x):
    return np.square(np.floor(x + 0.5))

# domain is [-20, 20] across all dimensions
def min(d):
    return -20.

def max(d):
    return 20.

def is_dimensionality_valid(D):
    return True

# min is [0, ..., 0] = 0
# though, seemingly, it is really [(-0.5, 0.5), ..., (0.5, 0.5)]?

# Tests:
import pytest as pt

def _test_min():
    for D in [2, 5, 10, 20, 50]:
        m = np.full(D, 0.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) <= function(p)

def _test_other():
    xs = [1., 2.]
    assert function(xs) == 5.

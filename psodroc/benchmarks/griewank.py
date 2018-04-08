import numpy as np
from numba import vectorize

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    _is = range(1, len(xs) + 1)
    return (np.sum(_inner1(xs)) / 4000.) \
        - np.prod(_inner2(xs, _is)) \
        + 1

@vectorize(['float64(float64)'])
def _inner1(x):
    return np.square(x)

@vectorize(['float64(float64, int64)'])
def _inner2(x, i):
    return np.cos(x / np.sqrt(i))

# domain = [-600.0, 600.0] across all dimensions
def min(d):
    return -600.

def max(d):
    return 600.

def is_dimensionality_valid(D):
    return True

# min = [0.0, ..., 0.0] = 0.0

# Tests:
import pytest as pt

def _test_min():
    for D in [1, 2, 5, 10, 20, 50]:
        m = np.full(D, 0.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [np.pi/2., np.pi/2.]
    assert function(xs) == pt.approx(1.0012337, abs=1e-9)

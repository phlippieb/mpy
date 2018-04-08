import numpy as np
from numba import vectorize

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return -np.sum(_inner(xs))

@vectorize(['float64(float64)'])
def _inner(x):
    return x * np.sin(np.sqrt(np.abs(x)))

# Domain is [-500, 500] across all dimensions
def min(d):
    return -500.

def max(d):
    return 500.

def is_dimensionality_valid(D):
    return True

# Minimum is [420.9687, ..., 420.9687]

# Tests:
import pytest as pt

def _test_min():
    for D in [1, 2, 5, 10, 20, 50]:
        m = np.full(D, 420.9687)
        y = -D * 418.9829
        assert function(m) == pt.approx(y, rel=1e-6)

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [1., 2., 3.]
    assert function(xs) == pt.approx(-5.77808281, rel=1e-9)

import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return np.sum([np.square(x) - 10 * np.cos(2 * np.pi * x) + 10 for x in xs])


# Domain is [-5.12, 5.12] across all dimensions
def min(d):
    return -5.12

def max(d):
    return 5.12

# Minimum is [0, ..., 0] = 0

# Tests:
import pytest as pt

def _test_min():
    for D in [1, 2, 5, 10, 20, 50]:
        m = np.full(D, 0.)
        assert function(m) == pt.approx(0.0)

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            m = np.full(D, 0.)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [np.pi / 2., np.pi / 2.]
    assert function(xs) == pt.approx(42.9885094392)

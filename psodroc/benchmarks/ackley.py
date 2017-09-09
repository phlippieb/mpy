# make division cast to double by default:
from __future__ import division
import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    assert D > 0, "ackley.function must have 1 or more dimensions."

    return -20. * np.exp(-.2 * (np.sqrt(sum(np.square(x) for x in xs) / D))) \
    - np.exp(sum(np.cos(2. * np.pi * x) for x in xs) / D) \
    + 20. \
    + np.exp(1)

# Domain is [-32.0, 32.0] across all dimensions
def min(d):
    return -32.

def max(d):
    return 32.

# Minimum is [0.0, ... 0.0] = 0.0

# Tests:
import pytest as pt

def _test_min():
    for D in [1, 2, 5, 10, 20, 50]:
        m = np.full(D, 0.)
        assert function(m) == pt.approx(0., abs=1e-15)

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [1, 2, 3]
    assert function(xs) == pt.approx(7.0164536, abs=1e-8)

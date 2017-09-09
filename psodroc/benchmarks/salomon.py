import numpy as np

# K. V. Price, R. M. Storn, and J. A. Lampinen. Appendix A.1: Unconstrained Uni-Modal Test Functions. In Differential Evolution A Practical Approach to Global Optimization, Natural Computing Series, pages 514-533. Springer-Verlag, Berlin, Germany, 2005.

def function(xs):
    s = np.sqrt(np.sum(np.square(xs)))
    return -np.cos(2. * np.pi * s) + (.1 * s) + 1.

# Domain is [-100, 100] across all dimensions
def min(d):
    return -100.

def max(d):
    return 100.

# Minimum is [0, ..., 0] = 0

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
    xs = [1., 2.]
    assert function(xs) == pt.approx(1.13618107303302, rel=1e-8)

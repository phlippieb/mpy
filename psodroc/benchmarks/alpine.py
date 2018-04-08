import numpy as np
from numba import vectorize

# S. Rahnamayan, H. R. Tizhoosh, and M. M. A. Salama. A novel population initialization method for accelerating evolutionary algorithms. Computers & Mathematics with Applications, 53(10):1605-1614, May 2007.

def function(xs):
    return sum(_inner(xs))

@vectorize(['float64(float64)'])
def _inner(x):
    return np.abs(x * np.sin(x) + .1 * x)

# domain = [-10.0, 10.0] across all dimensions
def min(d):
    return -10.

def max(x):
    return 10.

def is_dimensionality_valid(D):
    return True

# min = [0.0, ... 0.0] = 0.0

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
    xs = [1., 2.]
    assert function(xs) == 2.96006583845926

import numpy as np
from numba import vectorize

# S. Rahnamayan, H. R. Tizhoosh, and M. M. A. Salama. A novel population initialization method for accelerating evolutionary algorithms. Computers & Mathematics with Applications, 53(10):1605-1614, May 2007.

def function(xs):
    D = len(xs)
    assert D > 1, "Pathological.function must have 2 or more dimensions."
    return np.sum(_inner(xs[:-1], xs[1:]))

@vectorize(['float64(float64, float64)'])
def _inner(x1, x2):
    return 0.5 + ( \
        (np.square(np.sin(np.sqrt((100 * np.square(x1)) + np.square(x2)))) - 0.5) \
        / (1 + (0.001 * np.square(np.square(x1) - (2 * x1 * x2) + np.square(x2)))) \
    )

# domain = [-100, 100 across all dimensions]
def min(d):
    return -100.0

def max(d):
    return 100.0

def is_dimensionality_valid(D):
    # Pathological requires 2 or more dimensions.
    return D > 1

# min = [0, 0, ...] = 0

# Tests:
import pytest as pt

def _test_min():
    m = np.array([0., 0.])
    assert function(m) == 0.

    for i in range(100):
        p = np.random.uniform(low=min(0), high=max(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

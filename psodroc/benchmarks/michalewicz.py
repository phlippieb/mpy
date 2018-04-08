import numpy as np
from numba import vectorize

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs):
    return -np.sum(_inner(xs, range(1, len(xs) + 1)))

@vectorize(['float64(float64, int64)'])
def _inner(x, i):
    p = 10
    return np.sin(x) * np.power(np.sin((i*np.square(x)) / np.pi), (2 * p))

# domain = [0, pi] across all dimensions
def min(d):
    return 0.0

def max(d):
    return np.pi

def is_dimensionality_valid(D):
    return True

# min (D = 2) ~ -1.8013
# min (D = 5) ~ -4.6877
# min (D = 10) ~ -9.6602
# min (D = 30) ~ -29.6309

# Tests:
import pytest as pt

def _test_min():
    # The min input is known at 2 dimensions; assert:
    m2 = np.array([2.2, 1.57])
    assert function(m2) == pt.approx(-1.8013, abs=1e-3)

    # The min values are known at 5 and 10 dimensions; assert nothing is lower:
    m5 = -4.6877
    for i in range(100):
        p = np.random.uniform(low=min(0), high=max(0), size=5)
        assert m5 <= function(p)

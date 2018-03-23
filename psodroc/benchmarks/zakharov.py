import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs):
    a = np.sum(np.square(xs))
    b = np.sum((i*x)/2. for i, x in enumerate(xs, 1))
    return a + np.square(b) + np.power(b, 4.)

# domain = [-5, 10] across all dimensions
def min(d):
    return -5.

def max(d):
    return 10.
    
def is_dimensionality_valid(D):
    return True

# min = [0, ..., 0] = 0

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
    assert function(xs) == 50.3125

import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.


def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("eggholder.function must have exactly 2 dimensions.")
    x1 = xs[0]
    x2 = xs[1]

    return (-(x2 + 47.) * (np.sin(np.sqrt(np.abs((x2 + (x1/2.) + 47.)))))) \
    + (-x1 * (np.sin(np.sqrt(np.abs(x1 - x2 - 47.)))))

# domain = [-512.0, 512.0] across all dimensions
def min(d):
    return -512.

def max(d):
    return 512.

# min = [512, 404.23181] ~ -959.640662720823

# Tests:
import pytest as pt

def _test_assert_dimensions():
    xss = [[], [1], [1,2,3], [1,2,3,4,5]]
    for xs in xss:
        with pt.raises(Exception):
            function(xs)

def _test_min():
    m = np.array([512., 404.23181])
    assert function(m) == pt.approx(-959.640662720823)

    for i in range(100):
        p = np.random.uniform(low=min(0), high=min(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [200., 100.]
    assert function(xs) == pt.approx(-166.745338888944)

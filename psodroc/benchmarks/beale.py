import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs):
    D = len(xs)
    assert D == 2, "beale.function must have exactly 2 dimensions."
    (x1, x2) = (xs[0], xs[1])

    return np.square(1.5 - x1 + (x1 * x2)) \
    + np.square(2.25 - x1 + (x1 * np.square(x2))) \
    + np.square(2.625 - x1 + (x1 * np.power(x2, 3.)))

# domain = [-4.5, 4.5] across all dimensions
def min(d):
    return -4.5

def max(d):
    return 4.5
    
def is_dimensionality_valid(D):
    # Beale is only defined in 2 dimensions.
    return D == 2

# min = [3, 0.5] = 0

# Tests:
import pytest as pt
def _test_assert_dimensions():
    xss = [[], [1], [1,2,3], [1,2,3,4,5]]
    for xs in xss:
        with pt.raises(Exception):
            function(xs)

def _test_min():
    m = np.array([3., .5])
    assert function(m) == 0.

    for i in range(100):
        p = np.random.uniform(low=min(2), high=min(2), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = np.array([1., 2.])
    assert function(xs) == 126.4531250

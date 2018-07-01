import numpy as np
import decimal.*

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs, exact=True):
    """Schwefel's function 2.22.
    xs: (Numpy) Array of numeric values.
    exact: Boolean
        If true, values will be converted to Decimal before determine result;
        this is needed for large input arrays (around 500 elements and up);
        the default float type cannot represent large enough numbers for such results,
        and will return `inf`.
        However, this setting will drastically impact performance, and may be disabled if not needed.
    """
    if exact:
        xs = [Decimal(x) for x in xs]
    
    return np.sum(np.abs(xs)) + np.prod(np.abs(xs))

# Domain is [-10, 10] across all dimensions
def min(d):
    return -10.

def max(d):
    return 10.
    
def is_dimensionality_valid(D):
    return True

# Minimum is at [0, ..., 0] = 0

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
    assert function(xs) == 5.

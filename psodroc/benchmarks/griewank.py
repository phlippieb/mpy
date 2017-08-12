import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return (np.sum([x * x for x in xs]) / 4000.0) \
    - np.prod([np.cos(x / np.sqrt(i)) for i, x in enumerate(xs, 1)]) \
    + 1

# domain = [-600.0, 600.0] across all dimensions
def min(d):
    return -600.0

def max(d):
    return 600.0

# min = [0.0, ..., 0.0] = 0.0

# Tests:
import pytest as pt

def _test_min():
    for D in [1, 2, 5, 10, 20, 50]:
        m = np.full(D, 0.0)
        assert function(m) == pt.approx(0.0)

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            m = np.full(D, 0.)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [np.pi/2, np.pi/2]
    assert function(xs) == pt.approx(1.0012337)

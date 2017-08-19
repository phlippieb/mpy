import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("goldstein_price.function must have exactly 2 dimensions.")
    x1 = xs[0]
    x2 = xs[1]

    a1 = np.square(x1 + x2 + 1)
    a2 = 19. - (14. * x1) + (3. * np.square(x1)) - (14. * x2) + (6. * x1 * x2) + (3. * np.square(x2))
    a = 1. + (a1 * a2)
    b1 = np.square((2. * x1) - (3. * x2))
    b2 = 18. - (32. * x1) + (12. * np.square(x1)) + (48. * x2) - (36. * x1 * x2) + (27. * np.square(x2))
    b = 30. + (b1 * b2)
    return a * b

# domain = [-2.0, 2.0] across all dimensions
def min(d):
    return -2.

def max(d):
    return 2.

# min = [0, -1] = 3

# Tests:
import pytest as pt

def _test_assert_dimensions():
    xss = [[], [1], [1,2,3], [1,2,3,4,5]]
    for xs in xss:
        with pt.raises(Exception):
            function(xs)

def _test_min():
    m = np.array([0., -1.])
    assert function(m) == 3.

    for i in range(100):
        p = np.random.uniform(low=min(0), high=min(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [2., 2.]
    assert function(xs) == 76728.

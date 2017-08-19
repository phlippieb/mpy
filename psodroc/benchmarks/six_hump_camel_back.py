import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("six_hump_camel_back.function must have exactly 2 dimensions.")
    x1 = xs[0]
    x2 = xs[1]

    return (4. * np.square(x1)) \
    - (2.1 * np.power(x1, 4.)) \
    + (np.power(x1, 6.) / 3.) \
    + (x1 * x2) \
    - (4. * np.square(x2)) \
    + (4. * np.power(x2, 4.))

# Domain is [-5, 5] across all dimensions
def min(d):
    return -5.

def max(d):
    return 5.

# Minimum is at [0.08983, -0.7126] and [-0.08983, 0.7126], and is -1.03162842755

# Tests:
import pytest as pt

def _test_assert_dimensions():
    xss = [[], [1], [1,2,3], [1,2,3,4,5]]
    for xs in xss:
        with pt.raises(Exception):
            function(xs)

def _test_min():
    m1 = np.array([0.08983, -0.7126])
    m2 = np.array([-0.08983, 0.7126])
    y = -1.03162842755
    assert function(m1) == pt.approx(y)
    assert function(m2) == pt.approx(y)

    for i in range(100):
        p = np.random.uniform(low=min(0), high=min(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m1.all() or p.all() == m2.all() or (function(m1) < function(p) and function(m2) < function(p))

# def _test_other():
    xs = [0., 0.]
    assert function(xs) == 0.
    xs = [-1., 1.]
    assert function(xs) == pt.approx(1.2333333)

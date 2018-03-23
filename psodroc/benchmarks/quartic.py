import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return sum(i * np.power(x, 4.) for i, x in enumerate(xs, 1))

# domain = [-1.28, 1.28] across all dimensions
def min(d):
    return -1.28

def max(d):
    return 1.28
    
def is_dimensionality_valid(D):
    return True

# min = [0.0, ..., 0.0] = 0.0

# Tests:

def _test_min():
    for D in [1, 2, 3, 5, 10, 20, 30, 50, 100]:
        m = np.full(D, 0.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [2., 2., 2.]
    assert function(xs) == 96.

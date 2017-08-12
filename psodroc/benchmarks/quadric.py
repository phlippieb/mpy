import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    return np.sum([np.square(np.sum(xs[j] for j in range(i+1))) for i in range(D)])

# domain = [-100, 100] across all dimensions
def min(d):
    return -100.0

def max(d):
    return 100.0

# min = [0.0, ..., 0.0] = 0.0

# Tests:

def _test_min():
    for D in [1, 2, 3, 5, 10, 20, 30, 50, 100]:
        m = np.full(D, 0.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(0), high=max(0), size=D)
            m = np.full(D, 0.)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = [1., 2., 3.]
    assert function(xs) == 46.

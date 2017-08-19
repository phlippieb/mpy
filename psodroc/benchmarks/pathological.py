import numpy as np

# S. Rahnamayan, H. R. Tizhoosh, and M. M. A. Salama. A novel population initialization method for accelerating evolutionary algorithms. Computers & Mathematics with Applications, 53(10):1605-1614, May 2007.

def function(xs):
    D = len(xs)
    assert D > 1, "Pathological.function must have 2 or more dimensions."

    result = 0
    for xi, xi1 in zip(xs[:-1], xs[1:]):
        a = (np.square(np.sin(np.sqrt((100 * np.square(xi)) + np.square(xi1))))) - 0.5
        b = 1 + (0.001 * np.square(np.square(xi) - (2 * xi * xi1) + np.square(xi1)))
        result += 0.5 + (a / b)
    return result

# domain = [-100, 100 across all dimensions]
def min(d):
    return -100.0

def max(d):
    return 100.0

# min = [0, 0, ...] = 0

# Tests:
import pytest as pt

def _test_min():
    m = np.array([0., 0.])
    assert function(m) == 0.

    for i in range(100):
        p = np.random.uniform(low=min(0), high=max(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

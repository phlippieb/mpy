import numpy as np
from numba import vectorize

# N. Hansen and S. Kern. Evaluating the CMA Evolution Strategy on Multimodal Test Functions. In Proceedings of the 8th International Conference on Parallel Problem Solving from Nature, volume 3242 of Lecture Notes in Computer Science, pages 282-291. Springer Berlin / Heidelberg, 2004.

def function(xs):
    D = len(xs)
    return 10. * D + np.sum(_inner(_y(xs)))

@vectorize(['float64(float64)'])
def _y(x):
    return 10. * x if x > 0 else x


def _inner(y):
    return np.square(y) - (10. * np.cos(2. * np.pi * y))

# Domain is [-5, 5] across all dimensions
def min(d):
    return -5.

def max(d):
    return 5.

def is_dimensionality_valid(D):
    return True

# Minimum is [0, ..., 0] = 0

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
    assert function(xs) == 500.
    xs = [-1., -2.]
    assert function(xs) == 5.

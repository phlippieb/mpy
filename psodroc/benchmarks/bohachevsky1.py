# Bohachevsky, Ihor O., Mark E. Johnson, and Myron L. Stein. "Generalized simulated annealing for function optimization." Technometrics 28.3 (1986): 209-217.

import numpy as np

def function(xs):
    D = len(xs)
    assert D == 2, "bohachevsky1.function is only defined for 2 dimensions."

    x1 = xs[0]
    x2 = xs[1]

    return np.square(x1) \
        + 2 * np.square(x2) \
        - .3 * np.cos(3. * np.pi * x1) \
        - .4 * np.cos(4. * np.pi * x2) \
        + .7

# Domain is [-100, 100] for x1 and x2
def min(d):
    return -100.


def max(d):
    return +100.

# Minimum is at [0, 0] = 0

# Tests:
import pytest as pt
def _test_assert_dimensions():
    xss = [[], [1], [1,2,3], [1,2,3,4,5]]
    for xs in xss:
        with pt.raises(Exception):
            function(xs)


def _test_min():
    m = np.array([0., 0.])
    assert function(m) == 0.

    for i in range(100):
        p = np.random.uniform(low=min(2), high=min(2), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = np.array([1., 2.])
    assert function(xs) == 9.6

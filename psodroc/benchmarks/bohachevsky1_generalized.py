import numpy as np

# N. Hansen and S. Kern. Evaluating the CMA Evolution Strategy on Multimodal Test Functions. In Proceedings of the 8th International Conference on Parallel Problem Solving from Nature, volume 3242 of Lecture Notes in Computer Science, pages 282-291. Springer Berlin / Heidelberg, 2004.

def function(xs):
    D = len(xs)
    assert D > 1, "bohachevsky1_generalized.function must have 2 or more dimensions."

    return np.sum([ np.square(xi) + 2. * np.square(xi1) \
                 - .3 * np.cos(3. * np.pi * xi) \
                 - .4 * np.cos(4. * np.pi * xi1) \
                 + .7 \
                 for xi, xi1 in zip(xs[:-1], xs[1:]) ])

# domain = [-15.0, 15.0] across all dimensions
def min(d):
    return -15.

def max(d):
    return 15.
    
def is_dimensionality_valid(D):
    # Generalized Bohachevsky is only defined in 2 or more dimensions.
    return D > 1

# min = [0.0, ... 0.0] = 0.0

# Tests:
import pytest as pt
def _test_assert_dimensions():
    xss = [[], [1]]
    for xs in xss:
        with pt.raises(Exception):
            function(xs)


def _test_min():
    for D in [2, 5, 10, 20, 50]:
        m = np.full(D, 0.)
        assert function(m) == 0.

        for i in range(100):
            p = np.random.uniform(low=min(2), high=min(2), size=D)
            # Check that the minimum is less than the random point, unless the random point is the minimum:
            assert p.all() == m.all() or function(m) < function(p)

def _test_other():
    xs = np.array([1., 2.])
    assert function(xs) == 9.6

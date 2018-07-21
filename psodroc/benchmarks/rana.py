import numpy as np

# K. V. Price, R. M. Storn, and J. A. Lampinen. Appendix A.1: Unconstrained Uni-Modal Test Functions. In Differential Evolution A Practical Approach to Global Optimization, Natural Computing Series, pages 514-533. Springer-Verlag, Berlin, Germany, 2005.


def function(xs):
    D = len(xs)
    assert D > 1, 'rana.function must be called with 2 or more dimensions.'
    return np.sum(_inner(xi, xi1) for xi, xi1 in zip(xs[:-1], xs[1:]))


def _inner(xi, xi1):
    t1 = np.sqrt(np.abs(xi1 + xi + 1))
    t2 = np.sqrt(np.abs(xi1 - xi + 1))
    return (xi1 + 1) * np.cos(t2) * np.sin(t1) \
        + xi * np.cos(t1) * np.sin(t2)

# Domain is [-512, 512] across all dimensions


def min(d):
    return -512.


def max(d):
    return 512.


def is_dimensionality_valid(D):
    return D > 1

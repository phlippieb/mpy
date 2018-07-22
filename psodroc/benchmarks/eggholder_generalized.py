import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.


def function(xs):
    D = len(xs)
    assert is_dimensionality_valid(
        D), 'eggholder_generalized.function must be called with 2 or more dimensions.'

    return np.sum([_inner(x1, x2) for x1, x2 in zip(xs[:-1], xs[1:])])


def _inner(x1, x2):
    return (-(x2 + 47.) * (np.sin(np.sqrt(np.abs((x2 + (x1/2.) + 47.)))))) \
        + (-x1 * (np.sin(np.sqrt(np.abs(x1 - x2 - 47.)))))


# domain = [-512.0, 512.0] across all dimensions
def min(d):
    return -512.


def max(d):
    return 512.


def is_dimensionality_valid(D):
    return D > 1


# Tests:
import pytest as pt


def _test_min():
    m = np.array([512., 404.23181])
    assert function(m) == pt.approx(-959.640662720823, abs=1e-12)

    for i in range(100):
        p = np.random.uniform(low=min(0), high=min(0), size=2)
        # Check that the minimum is less than the random point, unless the random point is the minimum:
        assert p.all() == m.all() or function(m) < function(p)


def _test_other():
    xs = [200., 100.]
    assert function(xs) == pt.approx(-166.745338888944, abs=1e-12)

import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.


def function(xs):
    D = len(xs)
    result = 0
    for i in range(D):
        for k in _ks:
            result += (_as[k] * np.cos(_b1s[k] * (xs[i] + .5)))
    return result - D * _const_term

# Pre-calculated components (to speed up calculation):
# Do not change kMax during runtime!
_kMax = 20
_ks = range(_kMax+1)
_const_term = np.sum([np.power(.5, k) * np.cos(2. * np.pi * np.power(3, k) * .5) for k in _ks])
_as = [np.power(.5, k) for k in _ks]
_b1s = [2. * np.pi * np.power(3., k) for k in _ks]


# domain is [-0.5, -0.5] in all dimensions
def min(d):
    return -.5

def max(d):
    return .5

def is_dimensionality_valid(D):
    return True

# min = [0, ..., 0] = 0

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
    xs = [.1, .1]
    assert _function_old(xs, kMax=2) == pt.approx(1.786474508, rel=1e-9)

def _test_other():
    xss = [[.1, .1], [-.5, -.4, -.3, -.2, -.1, 0, .1, .2, .3, 4., .5]]
    for xs in xss:
        y = function(xs)
        y_old = _function_old(xs)
        assert y == pt.approx(y_old , abs=1e-15)

def _function_old(xs, kMax=20):
    ks = range(kMax+1) # Range is exclusive; function definition is inclusive

    return np.sum(np.sum(np.power(.5, k) * np.cos(2. * np.pi * np.power(3., k) * (x + .5)) for k in ks) for x in xs) \
    - (len(xs) * _constant_old(ks))

def _constant_old(ks):
    return np.sum([np.power(.5, k) * np.cos(2. * np.pi * np.power(3, k) * .5) for k in ks])

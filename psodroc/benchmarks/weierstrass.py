import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs, kMax=20):
    ks = range(kMax+1) # Range is exclusive; function definition is inclusive

    return np.sum(np.sum(np.power(.5, k) * np.cos(2. * np.pi * np.power(3., k) * (x + .5)) for k in ks) for x in xs) \
    - (len(xs) * _constant(ks))

def _constant(ks):
    return np.sum([np.power(.5, k) * np.cos(2. * np.pi * np.power(3, k) * .5) for k in ks])

# domain is [-0.5, -0.5] in all dimensions
def min(d):
    return -.5

def max(d):
    return .5

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
    assert function(xs, kMax=2) == pt.approx(1.786474508)

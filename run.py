# -*- coding: utf-8 -*-

import numpy as np

import psodroc.measures.neutrality as neutrality

import psodroc.benchmarks.step as step
import psodroc.benchmarks.spherical as spherical

# Dimensionality:
d = 5

# Spherical is not neutral at all:
print 'spherical:'
pn, lsn = neutrality.PN_LSN(
    spherical.function, spherical.min(0), spherical.max(0), d)
print '- PN =', pn
print '- LSN =', lsn

# Step contains neutrality, but it is not very connected.
print 'step:'
pn, lsn = neutrality.PN_LSN(step.function, step.min(0), step.max(0), d)
print '- PN =', pn
print '- LSN =', lsn


def neutral(xs):
    # A purely neutral function:
    return 0.


print 'neutral:'
pn, lsn = neutrality.PN_LSN(neutral, -10, 10, d)
print '- PN =', pn
print '- LSN =', lsn


def step_like(xs):
    # A step-like function with large steps:
    return np.ceil(xs[0])


print 'step-like:'
pn, lsn = neutrality.PN_LSN(step_like, -10, 10, d)
print '- PN =', pn
print '- LSN =', lsn

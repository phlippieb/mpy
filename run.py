# -*- coding: utf-8 -*-

import numpy as np

import psodroc.measures.neutrality as neutrality

import psodroc.benchmarks.step as step
import psodroc.benchmarks.spherical as spherical

# Dimensionality:
d = 5

# Spherical is not neutral at all:
print 'spherical:'
print '- PN =', neutrality.PN(
    spherical.function, spherical.min(0), spherical.max(0), d)
print '- LSN =', neutrality.LSN(
    spherical.function, spherical.min(0), spherical.max(0), d)

# Step contains neutrality, but it is not very connected.
print 'step:'
print '- PN =', neutrality.PN(step.function, step.min(0), step.max(0), d)
print '- LSN =', neutrality.LSN(step.function, step.min(0), step.max(0), d)


def neutral(xs):
    # A purely neutral function:
    return 0.


print 'neutral:'
print '- PN =', neutrality.PN(neutral, -10, 10, d)
print '- LSN =', neutrality.LSN(neutral, -10, 10, d)


def step_like(xs):
    # A step-like function with large steps:
    return np.ceil(xs[0])


print 'step-like:'
print '- PN =', neutrality.PN(step_like, -10, 10, d)
print '- LSN =', neutrality.LSN(step_like, -10, 10, d)

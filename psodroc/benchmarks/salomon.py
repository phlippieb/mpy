import numpy as np

# K. V. Price, R. M. Storn, and J. A. Lampinen. Appendix A.1: Unconstrained Uni-Modal Test Functions. In Differential Evolution A Practical Approach to Global Optimization, Natural Computing Series, pages 514-533. Springer-Verlag, Berlin, Germany, 2005.

def function(xs):
    return -np.cos(2 * np.pi * np.sum([np.square(x) for x in xs])) \
    + 0.1 * np.sqrt(np.sum([np.square(x) for x in xs])) \
    + 1

# Domain is [-100, 100] across all dimensions
def min(d):
    return -100

def max(d):
    return 100

# Minimum is [0, ..., 0] = 0

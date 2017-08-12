import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs):
    return np.sum([np.square(x) for x in xs]) \
    + np.square(np.sum([(i*x)/2 for i, x in enumerate(xs, 1)])) \
    + np.power(np.sum([(i*x)/2 for i, x in enumerate(xs, 1)]), 4)

# domain = [-5, 10] across all dimensions
def min(d):
    return -5.0

def max(d):
    return 10.0

# min = [0, ..., 0] = 0

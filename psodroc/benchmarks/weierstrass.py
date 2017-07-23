import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

ks = range(21) # i.e. [0, ..., 20]

def function(xs):
    return np.sum([np.sum([np.power(0.5, k) * np.cos(2 * np.pi * np.power(3, k) * (x + 0.5)) for k in ks]) for x in xs]) \
    - (len(xs) * _constant())

def _constant():
    return np.sum([np.power(0.5, k) * np.cos(2 * np.pi * np.power(3, k) * 0.5) for k in ks])

# domain is [-0.5, -0.5] in all dimensions
def min(d):
    return -0.5

def max(d):
    return 0.5

# min = [0, ..., 0] = 0

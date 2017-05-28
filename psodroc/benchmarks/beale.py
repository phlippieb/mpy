import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("beale.function must have exactly 2 dimensions.")
    x1 = xs[0]
    x2 = xs[1]

    return np.square(1.5 - x1 + (x1 * x2)) \
    + np.square(2.25 - x1 + (x1 * np.square(x2))) \
    + np.square(2.625 - x1 + (x1 * np.power(x2, 3)))

# domain = [-4.5, 4.5] across all dimensions
def min(d):
    return -4.5

def max(d):
    return 4.5
    
# min = [3, 0.5] = 0

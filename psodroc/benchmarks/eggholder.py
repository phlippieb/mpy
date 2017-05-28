import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.


def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("eggholder.function must have exactly 2 dimensions.")
    x1 = xs[0]
    x2 = xs[1]

    return (-(x2 + 47) * (np.sin(np.sqrt(np.abs((x2 + (x1/2) + 47)))))) \
    + (-x1 * (np.sin(np.sqrt(np.abs(x1 - (x2 + 47))))))

# domain = [-512.0, 512.0] across all dimensions
def min(d):
    return -512.0

def max(d):
    return 512.0

# min = [512, 404.23181] ~ -959.640662720823

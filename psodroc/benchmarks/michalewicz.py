import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def function(xs, p = 10):
    return -np.sum([np.sin(x) * np.power(np.sin(((i + 1) * np.square(x)) / np.pi), (2 * p)) for i, x in enumerate(xs)])

domain = [0, np.pi]
# min (D = 2) ~ -1.8013
# min (D = 5) ~ -4.6877
# min (D = 10) ~ -96602 # TODO: might be wrong -- try -9.6602
# min (D = 30) ~ -29.6309

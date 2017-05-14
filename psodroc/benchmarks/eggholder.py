import numpy as np

# S. K. Mishra. Performance of Repulsive Particle Swarm Method in Global Optimization of Some Important Test Functions: A Fortran Program. Technical report, Social Science Research Network (SSRN), August 2006.

def eggholder(x1, x2):
    return (-(x2 + 47) * (np.sin(np.sqrt(np.abs((x2 + (x1/2) + 47)))))) \
    + (-x1 * (np.sin(np.sqrt(np.abs(x1 - (x2 + 47))))))

domain = [-512, 512]
# min = [512, 404.23181] ~ -959.640662720823

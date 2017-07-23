import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return np.sum([np.square(x) - 10 * np.cos(2 * np.pi * x) + 10 for x in xs])


# Domain is [-5.12, 5.12] across all dimensions
def min(d):
    return -5.12

def max(d):
    return 5.12

# Minimum is [0, ..., 0] = 0

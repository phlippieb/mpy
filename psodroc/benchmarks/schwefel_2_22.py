import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return np.sum(xs) + np.prod(xs)

# Domain is [-10, 10] across all dimensions
def min(d):
    return -10

def max(d):
    return 10

# Minimum is at [0, ..., 0] = 0

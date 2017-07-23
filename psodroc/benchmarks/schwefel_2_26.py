import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return -np.sum([x * np.sin(np.sqrt(np.abs(x))) for x in xs])

# Domain is [-500, 500] across all dimensions
def min(d):
    return -500

def max(d):
    return 500

# Minimum is [420.9687, ..., 420.9687]

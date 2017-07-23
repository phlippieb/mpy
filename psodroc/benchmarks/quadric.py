import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return np.sum(np.square(np.sum(xs)))

# domain = [-100, 100] across all dimensions
def min(d):
    return -100.0

def max(d):
    return 100.0

# min = [0.0, ..., 0.0] = 0.0

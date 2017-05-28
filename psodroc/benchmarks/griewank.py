import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return (np.sum([x * x for x in xs]) / 4000.0) \
    - np.prod([np.cos(x / np.sqrt(i+1)) for i, x in enumerate(xs)]) \
    + 1

# domain = [-600.0, 600.0] across all dimensions
def min(d):
    return -600.0

def max(d):
    return 600.0

# min = [0.0, ..., 0.0] = 0.0

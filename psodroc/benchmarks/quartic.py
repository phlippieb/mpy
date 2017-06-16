import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return sum([i * np.power(x, 4) for i, x in enumerate(xs)])

# domain = [-100, 100] across all dimensions
def min(d):
    return -100

def max(d):
    return 100

# min = [0.0, ..., 0.0] = 0.0
    

import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82–102, July 1999.

def griewank(xs):
    return (np.sum([x * x for x in xs]) / 4000.0) \
    - np.prod([np.cos(x / np.sqrt(i+1)) for i, x in enumerate(xs)]) \
    + 1

domain = [-600, 600]
# min = [0.0, ..., 0.0] = 0.0

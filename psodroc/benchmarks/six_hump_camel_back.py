import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    if D != 2:
        raise Exception("six_hump_camel_back.function must have exactly 2 dimensions.")
    x1 = xs[0]
    x2 = xs[1]

    return (4 * np.square(x1)) \
    - (2.1 * np.power(x1, 4)) \
    + (np.power(x1, 6) / 3) \
    + (x1 * x2) \
    - (4 * np.square(x2)) \
    + (4 * np.power(x2, 4))

# Domain is [-5, 5] across all dimensions
def min(d):
    return -5.0

def max(d):
    return 5.0

# Minimum is at [0.08983, -0.7126] and [-0.08983, 0.7126], and is -1.03162842755

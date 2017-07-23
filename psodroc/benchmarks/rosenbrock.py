import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    D = len(xs)
    if D < 2:
        raise Exception("rosenbrock.function must have 2 or more dimensions.")

    return np.sum([(100 * np.square(xi1 - np.square(xi))) \
                   + np.square(xi - 1) \
                   for xi, xi1 in zip(xs[:-1], xs[1:])])


# Domain is [-2.048, 2.048] across all dimensions
def min(d):
    return -2.048

def max(d):
    return 2.048

# Minimum is [1, ..., 1] = 0

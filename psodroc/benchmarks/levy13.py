import numpy as np

# S. K. Mishra. Some new test functions for global optimization and performance of repulsive particle swarm method. Technical Report 2718, University Library of Munich, Germany, August 2006.

def function(xs):
    D = len(xs)
    if D < 2:
        raise Exception("levy.function must have 2 or more dimensions")

    return np.sum([np.square(np.sin(3 * np.pi * xi)) \
                   + np.square(xi - 1) * (1 + np.square(np.sin(3 * np.pi * xi1))) \
                   + np.square(xi1 - 1) * (1 + np.square(np.sin(2 * np.pi * xi1))) \
                   for xi, xi1 in zip(xs[:-1], xs[1:]) ])

# domain = [-10.0, 10.0] across all dimensions
def min(d):
    return -10.0

def max(d):
    return 10.0

# min = [1.0, ... 1.0] = 0.0

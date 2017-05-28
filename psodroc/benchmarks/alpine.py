import numpy as np

# S. Rahnamayan, H. R. Tizhoosh, and M. M. A. Salama. A novel population initialization method for accelerating evolutionary algorithms. Computers & Mathematics with Applications, 53(10):1605-1614, May 2007.

def function(xs):
    return sum([ np.abs(x * np.sin(x) + 0.1 * x) for x in xs ])

# domain = [-10.0, 10.0] across all dimensions
def min(d):
    return -10.0

def max(x):
    return 10.0

# min = [0.0, ... 0.0] = 0.0

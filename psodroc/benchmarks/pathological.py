import numpy as np

# S. Rahnamayan, H. R. Tizhoosh, and M. M. A. Salama. A novel population initialization method for accelerating evolutionary algorithms. Computers & Mathematics with Applications, 53(10):1605-1614, May 2007.

def function(xs):
    D = len(xs)
    if D < 2:
        raise Exception("Pathological.function must have 2 or more dimensions.")

    result = 0
    for xi, xi1 in zip(xs[:-1], xs[1:]):
        a = (np.square(np.sin(np.sqrt((100 * np.square(xi)) + np.square(xi1))))) - 0.5
        b = 1 + (0.001 * np.square(np.square(xi) - (2 * xi * xi1) + np.square(xi1)))
        result += 0.5 + (a / b)
    return result

# domain = [-100, 100 across all dimensions]
def min(d):
    return -100.0

def max(d):
    return 100.0

# min = [0, 0, ...] = 0

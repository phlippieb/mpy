# make division cast to double by default:
from __future__ import division
import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def functions(xs):
    D = len(xs)
    if D < 1:
        raise Exception("ackley.function must have 1 or more dimensions.")

    return -20 * np.exp(-0.2 * (np.sqrt(sum(x * x for x in xs) / D))) \
    - np.exp(sum([np.cos(2 * np.pi * x) for x in xs]) / D) \
    + 20 \
    + np.exp(1)

# domain = [-32.0, 32.0] across all dimensions
def min(d):
    return -32.0

def max(d):
    return 32.0

# min = [0.0, ... 0.0] = 0.0

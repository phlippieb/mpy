# make division cast to double by default:
from __future__ import division
import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def ackley(xs):
    D = len(xs)
    if D == 0:
        raise Exception("ackley.ackley may not have 0 dimensions")

    return -20 * np.exp(-0.2 * (np.sqrt(sum(x * x for x in xs) / D))) - np.exp(sum([np.cos(2 * np.pi * x) for x in xs]) / D) + 20 + np.exp(1)

domain = [-32.0, 32.0]
# min = [0.0, ... 0.0] = 0.0

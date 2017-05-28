import numpy as np

# K. A. De Jong. An analysis of the behavior of a class of genetic adaptive systems. PhD thesis, University of Michigan, Ann Arbor, MI, USA, 1975.

def function(xs):
    return sum([np.square(x) for x in xs ])

# domain = [-5.12, 5.12] across all dimensions
def min(d):
    return -5.12

def max(d):
    return 5.12

# min = [0.0, ... 0.0] = 0.0

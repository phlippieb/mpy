import numpy as np

# N. Hansen and S. Kern. Evaluating the CMA Evolution Strategy on Multimodal Test Functions. In Proceedings of the 8th International Conference on Parallel Problem Solving from Nature, volume 3242 of Lecture Notes in Computer Science, pages 282-291. Springer Berlin / Heidelberg, 2004.

def function(xs):
    D = len(xs)
    return 10 * D + np.sum([np.square(y(x)) - (10 * np.cos(2 * np.pi * y(x))) for x in xs])

def y(x):
    return 10 * x if x > 0 else x

# Domain is [-5, 5] across all dimensions
def min(d):
    return -5

def max(d):
    return 5

# Minimum is [0, ..., 0] = 0

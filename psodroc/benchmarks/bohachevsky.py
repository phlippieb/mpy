import numpy as np

# N. Hansen and S. Kern. Evaluating the CMA Evolution Strategy on Multimodal Test Functions. In Proceedings of the 8th International Conference on Parallel Problem Solving from Nature, volume 3242 of Lecture Notes in Computer Science, pages 282-291. Springer Berlin / Heidelberg, 2004.

def function(xs):
    D = len(xs)
    if D < 2:
        raise Exception("bohachevsky.function must have 2 or more dimensions.")

    return np.sum([ np.square(xi) + 2 * np.square(xi1) \
                 - 0.3 * np.cos(3 * np.pi * xi) \
                 - 0.4 * np.cos(4 * np.pi * xi1) \
                 + 0.7 \
                 for xi, xi1 in zip(xs[:-1], xs[1:]) ])

# domain = [-15.0, 15.0] across all dimensions
def min(d):
    return -15.0

def max(d):
    return 15.0
    
# min = [0.0, ... 0.0] = 0.0

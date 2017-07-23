import numpy as np

# X. Yao, Y. Liu, and G. Lin. Evolutionary Programming Made Faster. IEEE Transactions on Evolutionary Computation, 3(2):82-102, July 1999.

def function(xs):
    return np.sum([np.square(np.floor(x + 0.5)) for x in xs])

# domain is [-20, 20] across all dimensions
def min(d):
    return -20

def max(d):
    return 20

# min is [0, ..., 0] = 0
# though, seemingly, it is really [(-0.5, 0.5), ..., (-0.5, 0.5)]?

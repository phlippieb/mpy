import numpy as np

#

def function(xs):
    return -np.sum([x * np.sin(np.sqrt(np.abs(x))) for x in xs])

# Domain is [-500, 500] across all dimensions
def min(d):
    return -500

def max(d):
    return 500

# Minimum is [420.9687, ..., 420.9687]

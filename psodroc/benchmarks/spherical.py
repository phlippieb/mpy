import numpy as np

# K. A. De Jong. An analysis of the behavior of a class of genetic adaptive systems. PhD thesis, University of Michigan, Ann Arbor, MI, USA, 1975.
def spherical(xs):
    return sum([x*x for x in xs])

domain = [-5.12, 5.12]
# min = [0.0, ... 0.0] = 0.0

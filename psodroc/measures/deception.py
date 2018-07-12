import numpy as np
from scipy.spatial import distance
from decimal import *


def FDC(function, domain_min, domain_max, dimensions):
    # Sample some positions and determine their fitnesses.
    sample_size = 1000
    xs = np.random.uniform(low=domain_min, high=domain_max,
                           size=[sample_size, dimensions])
    fs = [function(x) for x in xs]

    # Determine the fittest position from the sample.
    x_star = xs[np.argmin(fs)]

    # Determine the distance from each position to the fittest position.
    ds = [distance.euclidean(x_star, x) for x in xs]
    ds = [Decimal(d) for d in ds]

    fm = np.mean(fs)
    dm = np.mean(ds)
    fm = Decimal(fm)
    dm = Decimal(dm)

    i_s = range(sample_size)
    numer = np.sum([(fs[i] - fm) * (ds[i] - dm) for i in i_s])
    denom = np.sqrt(np.sum([np.square(fs[i] - fm) for i in i_s])) * \
        np.sqrt(np.sum([np.square(ds[i] - dm) for i in i_s]))
    return numer / denom

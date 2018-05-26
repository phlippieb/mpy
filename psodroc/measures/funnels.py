import numpy as np
from scipy.spatial.distance import pdist as pairwise_distance
import itertools


def DM(function, domain_min, domain_max, dimensions):
    # This metric is used to estimate the presence of multiple funnels. It returns a value in the range [-disp_D, sqrt(D) - disp_D],
    # where D is the number of dimensions, and disp_D, a (pre-calculatable) constant, is the dispersion of a large uniform sample in
    # D dimensions. A dispersion metric > 0 indicates the presence of multiple funnels.
    # function: Callable. The fitness function to run the measure on.
    # domain_min: Float-like. The min of the function domain. Assumed to be the same in all dimensions.
    # domain_max: Float-like. The max of the function domain. Assumed to be the same in all dimensions.
    # dimensions: Int. The number of dimensions the function is defined in.
    # Returns: Float-like. A scalar in [-disp_D, sqrt(D) - disp_D]. A positive return value indicates the presence of multiple funnels.
    max_DM = None
    for s in np.arange(.05, .15, .001):
        DM = _DM(function, domain_min, domain_max, dimensions, 100, s)
        max_DM = DM if max_DM is None else max(max_DM, DM)
    return max_DM


def _DM(function, domain_min, domain_max, dimensions, n, s):
    # function: Callable. The fitness function to run the measure on.
    # domain_min: Float-like. The min of the function domain. Assumed to be the same in all dimensions.
    # domain_max: Float-like. The max of the function domain. Assumed to be the same in all dimensions.
    # dimensions: Int. The number of dimensions the function is defined in.
    # n: Int. The size of the large sample.
    # s: Float-like. The proportion of the large sample to use as the fittest sub-sample.
    # Returns: Float-like. A scalar in [-disp_D, sqrt(D) - disp_D]. A positive return value indicates the presence of multiple funnels.
    sample_positions = np.random.uniform(
        domain_min, domain_max, (n, dimensions))

    sample_fitnesses = np.array([function(sample_position)
                                 for sample_position in sample_positions])

    # Get the indices of the s smallest fitnesses from the sample, and use it to get the corresponding positions.
    s_size = int(n * s)
    s_indices = sample_fitnesses.argsort()[:s_size]
    s_positions = sample_positions[s_indices]

    # Normalize the positions to be in a domain of [0, 1]
    s_positions_normalized = _normalize(s_positions, domain_min, domain_max)

    dispersion = _dispersion(s_positions_normalized)
    return dispersion - _dispersion_const(dimensions)


def _normalize(xs, x_min, x_max):
    return [(x - x_min) / (x_max - x_min) for x in xs]


def _dispersion(xs):
    # The dispersion of a set of positions is the average pair-wise distance between those positions.

    # We need at least 2 positions to calculate pairwise distances
    if len(xs) < 2:
        return 0

    pairwise_distances = pairwise_distance(xs, 'euclidean')
    return np.average(pairwise_distances)


_dispersion_consts = {}


def _dispersion_const(D):
    # Returns a "pre-determined constant value for the dispersion of a large uniform random sample in a D-dimensional search space, normalised to [0, 1] in all dimensions"
    # We will not be pre-determining constant values for every possible D, so we will calculate it instead.
    if D in _dispersion_consts:
        return _dispersion_consts[D]
    else:
        # Uniformly sample 1000 D-dimensional positions in [0, 1]
        xs = np.random.uniform(0., 1., (1000, D))
        # Calculate, store, and return the dispersion of such a sample
        _dispersion_consts[D] = _dispersion(xs)
        return _dispersion_consts[D]

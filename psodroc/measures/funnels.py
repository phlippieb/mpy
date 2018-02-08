import numpy as np
from scipy.spatial.distance import pdist as pairwise_distance
from numba import jit

# This metric is used to estimate the presence of multiple funnels. It returns a value in the range [-disp_D, sqrt(D) - disp_D],
# where D is the number of dimensions, and disp_D, a (pre-calculatable) constant, is the dispersion of a large uniform sample in
# D dimensions. A dispersion metric > 0 indicates the presence of multiple funnels.
# Parameter function:   The fitness function to run the measure on.
# Parameter domain_min: The min of the function domain. Assumed to be the same in all dimensions.
# Parameter domain_max: The max of the function domain. Assumed to be the same in all dimensions.
# Parameter dimensions: The number of dimensions the function is defined in.
# Returns:              A scalar in [-disp_D, sqrt(D) - disp_D]. A positive return value indicates the presence of multiple funnels.
def dispersion_metric(function, domain_min, domain_max, dimensions):
    return _dispersion_metric(function, domain_min, domain_max, dimensions, 1000, 100)
    
def _dispersion_metric(function, domain_min, domain_max, dimensions, n, s):
    sample_positions = np.random.uniform(domain_min, domain_max, (n, dimensions))
    sample_fitnesses = np.array([function(sample_position) for sample_position in sample_positions])
    
    # Get the indices of the s smallest fitnesses from the sample, and use it to get the corresponding positions.
    s_indices = sample_fitnesses.argsort()[:s]
    s_positions = sample_positions[s_indices]
    
    # Normalise the positions to be in a domain of [0, 1]
    s_positions_normalized = _normalize(s_positions, domain_min, domain_max)
    
    dispersion = _dispersion(s_positions_normalized)
    return dispersion - _dispersion_const(dimensions)
    # return 0

def _normalize(xs, x_min, x_max):
    return [(x - x_min) / (x_max - x_min) for x in xs]
    
# The dispersion of a set of positions is the average pair-wise distance between those positions.
@jit # (Make things faster)
def _dispersion(xs):
    # We need at least 2 positions to calculate pairwise distances
    if len(xs) < 2:
        return 0
    
    pairwise_distances = pairwise_distance(xs, 'euclidean')
    return np.average(pairwise_distances)
    
# Returns a "pre-determined constant value for the dispersion of a large uniform random sample in a D-dimensional search space, normalised to [0, 1] in all dimensions"
# We will not be pre-determining constant values for every possible D, so we will calculate it instead.
def _dispersion_const(D):
    if D in _dispersion_consts:
        return _dispersion_consts[D]
    else:
        # Uniformly sample 1000 D-dimensional positions in [0, 1]
        xs = np.random.uniform(0., 1., (1000, D))
        # Calculate, store, and return the dispersion of such a sample
        _dispersion_consts[D] = _dispersion(xs)
        return _dispersion_consts[D]
    
_dispersion_consts = {}

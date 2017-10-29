import numpy as np

# This file contains diversity measures that can be taken on a particle swarm.

# Given a 2-d array of particle positions (with d-1 corresponding to the particles, and d-2 to the position dimensions), this function returns the average distance between each particle's position and the swarm's average position (i.e. the "centre").
def avg_distance_around_swarm_centre(xs):
    assert len(np.shape(xs)) == 2, \
        "Particles must be a 2-d numpy array, with d-1 corresponding to the particles, and d-2 to the dimensions."
    assert np.shape(xs)[0] > 0, \
        "Swarm must have more than zero particles."
    assert np.shape(xs)[1] > 0, \
        "Swarm must have more than zero dimensions."
    
    # Calculate the "swarm centre" once-off:
    dimension_averages = np.mean(xs, axis=0)
    
    # Return the average distance between each particle and the swarm centre:
    return np.average([np.sqrt(sum(np.square(d - dimension_averages[k]) for (k, d) in enumerate(x))) for x in xs])

# Tests:
import pytest as pt

def _test_assert_dimensions():
    # Examples of invalid parameter shapes:
    xss = [
        [0, 1],
        [[[0]], [[1]]]
    ]
    for xs in xss:
        with pt.raises(Exception):
            avg_distance_around_swarm_centre(xs)

def _test_assert_not_empty():
    xss = [
        [],
        [[]]
    ]
    for xs in xss:
        with pt.raises(Exception):
            avg_distance_around_swarm_centre(xs)
        
def _test_zero_distance():
    xs = [[0., 1., 2.], [0., 1., 2.], [0., 1., 2.]]
    assert avg_distance_around_swarm_centre(xs) == 0, \
        "Expected a swarm of particles with identical positions to yield a zero avg distance to the swarm centre."

def _test_lonely_swarm():
    xs = [[0., 1., 2., 4.]]
    assert avg_distance_around_swarm_centre(xs) == 0, \
        "Expected a swarm with just one particle to yield a zero avg distance to the swarm centre."
    
def _test_other():
    xs = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    assert avg_distance_around_swarm_centre(xs) == 1
    
    xs = [[-2.5, 1.5], [-0.5, 1.5], [1.5, -0.5], [1.5, -2.5], [1.5, 3.5], [1.5, 5.5], [5.5, 1.5], [3.5, 1.5]]
    assert avg_distance_around_swarm_centre(xs) == 3
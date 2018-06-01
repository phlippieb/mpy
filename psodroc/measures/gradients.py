import progressive_manhattan_walk as manhattan
import numpy as np


def G_measures(function, domain_min, domain_max, dimensions):
    starting_zones = manhattan.get_starting_zones(dimensions)

    # Approach 1:
    # s = 0.001
    # num_steps = manhattan.get_num_steps(dimensions, s)
    # step_size = manhattan.get_step_size(domain_min, domain_max, s)

    # Approach 2:
    num_steps = 1000
    step_size = ((domain_max - domain_min) * dimensions) / 1000

    walks = [manhattan.walk(dimensions, domain_min, domain_max, num_steps,
                            step_size, starting_zone) for starting_zone in starting_zones]

    # TODO: in Katherine's paper, these are normalised, which mine now contradicts.
    #       - fix and update my thesis.

    # Determine the gradient between each consecutive step.
    gradients = _gradients(function, domain_min,
                           domain_max, dimensions, walks, step_size)

    # Use the absolute value of each gradient;
    # this is because we don't care about the direction of the gradients,
    # and don't want "ups" and "downs" to cancel out.
    abs_gradients = np.absolute(gradients)

    # Simply determine and return the average and standard deviation of the absolute gradients.
    avg = np.average(abs_gradients)
    dev = np.std(abs_gradients)
    return avg, dev


def _gradients(function, domain_min, domain_max, dimensions, walks, step_size):
    gradients = []
    f_range = _f_range(function, walks)
    x_range = domain_max - domain_min

    for walk in walks:
        fs = [function(xs) for xs in walk]
        f1s = fs[:-1]  # f_0, f_1, ..., f_n-1
        f2s = fs[1:]  # f_1, f_2, ..., f_n
        gradients += [_gradient(
            f1, f2, f_range, step_size, x_range, dimensions)
            for f1, f2 in zip(f1s, f2s)]

    return gradients


def _f_range(function, walks):
    f_min = None
    f_max = None
    for walk in walks:
        for xs in walk:
            f = function(xs)
            f_min = f if f_min is None else min(f_min, f)
            f_max = f if f_max is None else max(f_max, f)
    return f_max - f_min


def _gradient(f1, f2, f_range, s, x_range, n):
    numer = (f2 - f1) / f_range
    denom = s / (n * x_range)
    return numer / denom

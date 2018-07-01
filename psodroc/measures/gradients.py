import progressive_manhattan_walk as manhattan
import numpy as np


def G_measures(function, domain_min, domain_max, dimensions, step_size_fraction=1e-3, verbose=False):
    starting_zones = manhattan.get_starting_zones(dimensions)

    step_size = ((domain_max - domain_min) * dimensions) * step_size_fraction
    num_steps = int(1. / step_size_fraction)

    # Cut it off at 200 walks; high dimensionalities take too long otherwise.
    starting_zones = starting_zones[:200]
    walks = []
    for (i, starting_zone) in enumerate(starting_zones):
        if verbose:
            print '[gradients] Walking', i+1, 'of', len(starting_zones), '...'
        
        walk = manhattan.walk(dimensions, domain_min,
                              domain_max, num_steps, step_size, starting_zone)
        walks.append(walk)

    # Determine the gradient between each consecutive step.
    if verbose:
        print '[gradients] getting gradients...'
    gradients = _gradients(function, domain_min,
                           domain_max, dimensions, walks, step_size)

    # Use the absolute value of each gradient;
    # this is because we don't care about the direction of the gradients,
    # and don't want "ups" and "downs" to cancel out.
    if verbose:
        print '[gradients] getting gradient absolutes...'
    abs_gradients = np.absolute(gradients)

    # Simply determine and return the average and standard deviation of the absolute gradients.
    if verbose:
        print '[gradients] getting avg...'
    avg = np.average(abs_gradients)
    if verbose:
        print '[gradients] getting std deviation...'
    dev = np.std(abs_gradients)
    return avg, dev


def _gradients(function, domain_min, domain_max, dimensions, walks, step_size):
    gradients = []
    f_range = _f_range(function, walks)
    x_range = domain_max - domain_min

    for (i, walk) in enumerate(walks):
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

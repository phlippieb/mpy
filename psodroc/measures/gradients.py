import progressive_manhattan_walk as manhattan
import numpy as np


def G_measures(function, domain_min, domain_max, dimensions):
    s = 0.001
    starting_zones = manhattan.get_starting_zones(dimensions)
    num_steps = manhattan.get_num_steps(dimensions, s)
    step_size = manhattan.get_step_size(domain_min, domain_max, s)
    walks = [manhattan.walk(dimensions, domain_min, domain_max, num_steps,
                            step_size, starting_zone) for starting_zone in starting_zones]

    # TODO: in Katherine's paper, these are normalised, which mine now contradicts.
    #       - fix and update my thesis.

    # Determine the gradient between each consecutive step.
    gradients = _gradients2(function, domain_min,
                            domain_max, dimensions, walks, step_size)
    # Use the absolute value of each gradient;
    # this is because we don't care about the direction of the gradients,
    # and don't want "ups" and "downs" to cancel out.
    abs_gradients = np.absolute(gradients)

    # Simply determine and return the average and standard deviation of the absolute gradients.
    return np.average(abs_gradients), np.std(abs_gradients)


def _gradients2(function, domain_min, domain_max, dimensions, walks, step_size):
    gradients = []

    for walk in walks:

        fitnesses = [function(xs) for xs in walk]

        # The gradient between each steps is normalised.

        # Obtain the min and max fitness.
        fitness_range = np.max(fitnesses) - np.min(fitnesses)

        # Obtain the total Manhattan distance between the position vectors defining the bounds of the search space.
        bounds_range = np.sum(
            [domain_max - domain_min for i in range(dimensions)])
        denominator = step_size / bounds_range

        f1s = fitnesses[:-1]
        f2s = fitnesses[1:]

        walk_gradients = [_gradient2(f1, f2, np.max(fitnesses), np.min(
            fitnesses), step_size, domain_max, domain_min, dimensions) for f1, f2 in zip(f1s, f2s)]
        gradients += walk_gradients

    return gradients


def _gradient2(f1, f2, fmax, fmin, s, xmax, xmin, n):
    numerator = (f2 - f1) / (fmax - fmin)
    denominator = s / (1 * (xmax - xmin))
    return numerator / denominator

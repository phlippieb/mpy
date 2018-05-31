import numpy as np


def single_walk(n, domain_min, domain_max, num_steps, s, starting_zone):
    # Perform a random walk.
    # Katherine Mary Malan. Characterising continuous optimisation problems for parti- cle swarm optimisation performance prediction. PhD thesis, University of Pretoria, 2014.
    # n: Int. The number of dimensions of the problem.
    # domain_min: Int. The domain minimum of the problem. The same domain min is used in each dimension.
    # domain_max: Int. The domain maximum of the problem. The same domain min is used in each dimension.
    # num_steps: Int. The number of steps in the walk.
    # s: Float-like. The step size. Fixed.
    # starting_zone: [Int]. A binary array of size n. Specifies the starting zone of the walk. The starting zone is a hypercube in one corner of the problem space. Each bit in the array specifies, for each corresponding dimension, whether the starting zone is in the lower or upper half of that dimension's domain; a 0 indicates that the walk should start in [domain_min, domain_range/2] in that dimension, and a 1 indicates that it should start in [domain_range/2, domain_max].

    # An array of num_steps n-dimensional vectors for storing results
    walk = np.zeros([num_steps, n])

    # The mid-point of the domain.
    domain_mid = (domain_max - domain_min) / 2.

    # Set the initial position of the walk.
    for i in range(n):
        # Get the range for the starting zone in this dimension based on the corresponding bit in `starting_zone`.
        low, high = (domain_min, domain_mid) if starting_zone[i] == 0 else (
            domain_mid, domain_max)

        # Choose a random point in the starting zone.
        r = np.random.uniform(low=low, high=high)

        # Set the initial position in this dimension to the random point.
        walk[0][i] = r

    # Set the initial position to be against the edge in a random dimension.
    rD = np.random.randint(n)
    walk[0][rD] = domain_max if starting_zone[rD] == 1 else domain_min

    # Add steps to the walk.
    for step in range(1, num_steps):
        # Select a random dimension.
        rD = np.random.randint(n)

        # Update each dimension component.
        for i in range(n):
            if i == rD:
                # Take a fixed-size step away from the starting zone in the randomly-selected dimension.
                direction = +1. if starting_zone[i] == 1 else -1.
                walk[step][i] = walk[step-1][i] + (direction * s)

                # If the boundary was overstepped, mirror the step and flip the corresponding starting zone bit.
                if walk[step][i] < domain_min or domain_max < walk[step][i]:
                    walk[step][i] = walk[step-1][i] - (direction * s)
                    starting_zone[i] = 1 if starting_zone[i] == 0 else 0

            else:
                # Do not update position in non-selected dimensions.
                walk[step][i] = walk[step-1][i]

    # All steps are complete. Return the walk.
    return walk


def multiple_walks(n, domain_min, domain_max, s):
    # Performs `n` walks.
    # The starting zone of each walk is chosen to maximize the coverage;
    # see Katherine Mary Malan. Characterising continuous optimisation problems for parti- cle swarm optimisation performance prediction. PhD thesis, University of Pretoria, 2014.
    # Out of 2^n starting zones, only every (2^n)/n-th zone is used.
    # n: Int. The number of dimensions of the problem space.
    # domain_min, domain_max: Float-like. The domain of the problem space.
    # s: Float-like. The fixed step size as a proportion of the domain range; e.g. 0.1 for a 10-th of the domain range.
    increment = (2 ** n) / n
    starting_zones = np.zeros([n, n], dtype=int)
    for z in range(n):
        zone_number = z * increment
        zone_string = "{0:b}".format(zone_number)
        reverse_string = zone_string[::-1]
        for (i, c) in enumerate(reverse_string):
            starting_zones[z][n-i-1] = int(c)

    step_size = (domain_max - domain_min) * s
    num_steps = int(1. / s) * n * 2
    walks = np.zeros([n, num_steps, n])
    for (i, starting_zone) in enumerate(starting_zones):
        walks[i] = single_walk(n, domain_min, domain_max,
                               num_steps, step_size, starting_zone)

    return walks

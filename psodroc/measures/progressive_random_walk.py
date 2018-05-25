import numpy as np


def progressive_random_walk(n, domain_min, domain_max, num_steps, s, starting_zone):
    # Perform a random walk.
    # Katherine Mary Malan. Characterising continuous optimisation problems for parti- cle swarm optimisation performance prediction. PhD thesis, University of Pretoria, 2014.
    # n: Int. The number of dimensions of the problem.
    # domain_min: Int. The domain minimum of the problem. The same domain min is used in each dimension.
    # domain_max: Int. The domain maximum of the problem. The same domain min is used in each dimension.
    # num_steps: Int. The number of steps in the walk.
    # s: Float-like. The step size upper bound.
    # starting_zone: [Int]. A binary array of size n. Specifies the starting zone of the walk. The starting zone is a hypercube in one corner of the problem space. Each bit in the array specifies, for each corresponding dimension, whether the starting zone is in the lower or upper half of that dimension's domain; a 0 indicates that the walk should start in [domain_min, domain_range/2] in that dimension, and a 1 indicates that it should start in [domain_range/2, domain_max].

    # An array of s n-dimensional vectors for storing results
    walk = np.zeros([s, n])

    # Keep track of the middle of the domain.
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
    walk[0][rD] = domain_max if starting_zone[rD] == 1 else domain_main

    # Add steps to the walk.
    for step in range(1, num_steps):
        for i in range(n):
            # Get a random step size in [0, s) in the direction away from the starting zone.
            direction = 1. if starting_zone[i] == 0 else -1.
            r = np.random.uniform(low=0, high=s) * direction

            # Add the step size to the previous step to get the new step.
            walk[step][i] = walk[step-1][i] + r

            # If the step is outside the problem domain, handle.
            if walk[step][i] < domain_min or domain_max < walk[step][i]:
                # If the minimum boundary was overstepped, *this* value will be negative:
                e1 = walk[step][i] - domain_min
                # Else, *this* value will be negative:
                e2 = domain_max - walk[step][i]

                # Determine the amount that the boundary was overstepped with as `e`,
                # as well as the index the boundary that was overstepped (min or max) as `ei`.`
                e, ei = (np.min([e1, e2]), np.argmin([e1, e2]))

                # Mirror the position inside the domain.
                mirrored_step = 2 * e * (1 if ei == 1 else -1)
                walk[step][i] += mirrored_step

                # Flip the corresponding bit in the starting zone to guide the walk in the opposite direction.
                starting_zone[i] *= -1

    # All steps are complete. Return the walk.
    return walk

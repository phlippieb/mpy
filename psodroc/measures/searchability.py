import numpy as np
import warnings


def FCIs(function, domain_min, domain_max, dimensions):
    """
    Performs the following sets of fitness cloud index measurements:
    - 30 x FCI_soc measurements (with social-only PSO updates)
    - 30 x FCI_cog measurements (with cognitive-only PSO updates)
    Returns the following:
    1. The mean of the FCI_soc measurements
    2. The mean of the FCI_cog measurements
    3. The mean of the standard deviation of the FCI_soc and the FCI_cog measurements, respectively.
    """

    num_samples = 30
    swarm_size = 500
    num_updates = 2

    fci_socs = [FCI_soc(function, domain_min, domain_max, dimensions, swarm_size, num_updates)
                for _ in range(num_samples)]

    fci_cogs = [FCI_cog(function, domain_min, domain_max, dimensions, swarm_size, num_updates)
                for _ in range(num_samples)]

    fci_soc_mean = np.mean(fci_socs)
    fci_cog_mean = np.mean(fci_cogs)
    fci_sigma = FCI_sigma(fci_socs, fci_cogs)

    return fci_soc_mean, fci_cog_mean, fci_sigma


def FCI_sigma(FCI_socs, FCI_cogs):
    # Given a list each of FCI_soc and FCI_cog measurements,
    # this determines the standard deviation of each list of measurements
    # and returns the mean of those standard deviations.
    FCI_soc_dev = np.std(FCI_socs)
    FCI_cog_dev = np.std(FCI_cogs)
    return np.mean([FCI_soc_dev, FCI_cog_dev])


import psodroc.pso.social_only_pso as spso


def FCI_soc(function, domain_min, domain_max, dimensions, swarm_size, num_updates=2):
    """
    Get a single fitness cloud index measurement using two position updates with social-only PSO.
    """

    # Set up the PSO.
    spso.function = function
    spso.lower_bound = domain_min
    spso.upper_bound = domain_max
    spso.num_dimensions = dimensions
    spso.init_swarm(swarm_size)
    spso.init_pso_defaults()

    # Record the initial positions.
    initial_positions = spso.positions

    # Record the final positions after the specified number of position updates.
    for _ in range(num_updates):
        spso.iterate()
    final_positions = spso.positions

    return _FCI(initial_positions, final_positions, function, domain_min, domain_max, swarm_size)


import psodroc.pso.cognitive_only_pso as cpso


def FCI_cog(function, domain_min, domain_max, dimensions, swarm_size, num_updates=2):
    """
    Get a single fitness cloud index measurement using two position updates with social-only PSO.
    """

    # Set up the PSO.
    cpso.init_search_space(function, dimensions, domain_min, domain_max)
    cpso.init_swarm(swarm_size)
    cpso.init_pso_defaults()

    # Record the initial positions.
    initial_positions = cpso.positions

    # Artificially generate a nearby pbest for each particle to get things going.
    for i in range(swarm_size):
        # Choose a random nearby position.
        r = .1 * (domain_max - domain_min)
        x = cpso.positions[i]
        z = np.random.normal(x, scale=r, size=dimensions)

        # My edit: do not use z as a position or a pbest if it is out of bounds;
        # simply retry until it's in bounds.
        while not _is_within_bounds(z, domain_min, domain_max):
            z = np.random.normal(x, scale=r, size=dimensions)

        # Choose the fittest position between x and z to be the particle's pbest,
        # and the other position to be the particle's position.
        # (Note: at this point, pbest already refers to x, so we only need to set z where appropriate.)
        f_x = function(x)
        f_z = function(z)
        if f_x < f_z:
            # Leave the fitter x as the pbest, and move the particle to z.
            cpso.positions[i] = z
            cpso.fitnesses[i] = f_z
        else:
            # Use the fitter z as the pbest, and leave the particle at x.
            cpso.pbest_positions[i] = z
            cpso.pbest_fitnesses[i] = f_z

    # Record the final positions after the specified number of position updates.
    for _ in range(num_updates):
        cpso.iterate()

    final_positions = cpso.positions

    return _FCI(initial_positions, final_positions, function, domain_min, domain_max, swarm_size)


def _FCI(initial_positions, final_positions, function, domain_min, domain_max, swarm_size):
    # Find the indices of the particles that have not left the search space.
    # Only these particles will be considered.
    valid_indices = []
    for index in range(swarm_size):
        position = final_positions[index]
        if _is_within_bounds(position, domain_min, domain_max):
            valid_indices.append(index)

    if len(valid_indices) == 0:
        warnings.warn("FCI_cog: All particles left the search space.")
        return 0.

    # Determine the fitnesses of all valid initial and final points.
    initial_fitnesses = [function(x) for x in initial_positions[valid_indices]]
    final_fitnesses = [function(x) for x in final_positions[valid_indices]]

    # [initial_fitnesses, final_fitnesses].T is now the fitness cloud.
    # The fitness cloud index is the proportion of fitnesses that improved.
    improvements = [1 if f_final < f_initial else 0
                    for f_final, f_initial in zip(final_fitnesses, initial_fitnesses)]
    num_improvements = np.sum(improvements)
    return float(num_improvements) / float(len(final_fitnesses))


def _is_within_bounds(position, lower, upper):
    for component in position:
        if component < lower or component > upper:
            return False
    return True

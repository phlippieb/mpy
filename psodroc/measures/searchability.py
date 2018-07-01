import numpy as np
import warnings


def FCI_sigma(FCI_socs, FCI_cogs):
    # Given a list each of FCI_soc and FCI_cog measurements,
    # this determines the standard deviation of each list of measurements
    # and returns the mean of those standard deviations.
    FCI_soc_dev = np.std(FCI_socs)
    FCI_cog_dev = np.std(FCI_cogs)
    return np.mean([FCI_soc_dev, FCI_cog_dev])


import psodroc.pso.social_only_pso as spso


def FCI_soc(function, domain_min, domain_max, dimensions, swarm_size=500, num_updates=2):
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

    # Record the initial fitnesses.
    initial_fitnesses = [function(x) for x in spso.positions]

    # Perform position updates.
    for _ in range(num_updates):
        spso.iterate()

        # Repair positions that have left the search space to be on the boundary.
        repaired_positions, repaired_indices = _repaired_positions_and_indices(
            spso.positions, domain_min, domain_max)
        spso.positions = repaired_positions

        # Update the swarm gbests according to the new (repaired) positions.
        spso.fitnesses = [function(x) for x in spso.positions]
        for i in range(swarm_size):
            if spso.fitnesses[i] < spso.gbest_fitness:
                spso.gbest_fitness = spso.fitnesses[i]
                spso.gbest_position = spso.positions[i]

        # Reset the repaired particles' velocities so that they can still return to the search space.
        for repaired_index in repaired_indices:
            spso.velocities[repaired_index] = np.zeros(dimensions)

    # Record the final fitnesses after the specified number of position updates.
    final_fitnesses = [function(x) for x in spso.positions]

    # Normalise fitnesses between the min and max encountered.
    min_fitness = min(initial_fitnesses + final_fitnesses)
    max_fitness = max(initial_fitnesses + final_fitnesses)
    initial_fitnesses = [(initial_fitness - min_fitness) / \
        (max_fitness - min_fitness) for initial_fitness in initial_fitnesses]
    final_fitnesses = [(final_fitness - min_fitness) / \
        (max_fitness - min_fitness) for final_fitness in final_fitnesses]

    fci = _FCI(initial_fitnesses, final_fitnesses)
    return fci


import psodroc.pso.cognitive_only_pso as cpso


def FCI_cog(function, domain_min, domain_max, dimensions, swarm_size=500, num_updates=2):
    """
    Get a single fitness cloud index measurement using two position updates with social-only PSO.
    """

    # Set up the PSO.
    cpso.init_search_space(function, dimensions, domain_min, domain_max)
    cpso.init_swarm(swarm_size)
    cpso.init_pso_defaults()

    # Record the initial fitnesses.
    initial_fitnesses = [function(x) for x in cpso.positions]

    from decimal import *
    initial_fitnesses = [Decimal(f) for f in initial_fitnesses]

    # Artificially generate a nearby pbest for each particle to get things going.
    for i in range(swarm_size):
        # Choose a random nearby position.
        r = .1 * (domain_max - domain_min)
        x = cpso.positions[i]
        z = np.random.normal(x, scale=r, size=dimensions)
        # Repair neighbours that are out of bounds to be on the boundary.
        z = _repaired_position(z, domain_min, domain_max)

        # Choose the fittest position between x and z to be the particle's pbest,
        # and the other position to be the particle's position.
        # (Note: at this point, pbest already refers to x, so we only need to set z where appropriate.)
        f_z = function(z)
        if function(x) < f_z:
            # Leave the fitter x as the pbest, and move the particle to z.
            cpso.positions[i] = z
            cpso.fitnesses[i] = f_z
        else:
            # Use the fitter z as the pbest, and leave the particle at x.
            cpso.pbest_positions[i] = z
            cpso.pbest_fitnesses[i] = f_z

    # Record the final fitnesses after the specified number of position updates.
    for _ in range(num_updates):
        cpso.iterate()

        # Repair positions that have left the search space to be on the boundary.
        repaired_positions, repaired_indices = _repaired_positions_and_indices(
            cpso.positions, domain_min, domain_max)
        cpso.positions = repaired_positions

        # Update the swarm state according to the new (repaired) positions.
        cpso.fitnesses = [function(x) for x in cpso.positions]
        for i in range(swarm_size):
            if cpso.fitnesses[i] < cpso.pbest_fitnesses[i]:
                cpso.pbest_fitnesses[i] = cpso.fitnesses[i]
                cpso.pbest_positions[i] = cpso.positions[i]

        # Reset the repaired particles' velocities so that they can still return to the search space.
        for repaired_index in repaired_indices:
            cpso.velocities[repaired_index] = np.zeros(dimensions)

    final_fitnesses = [function(x) for x in cpso.positions]

    min_fitness = min(initial_fitnesses + final_fitnesses)
    max_fitness = max(initial_fitnesses + final_fitnesses)

    initial_fitnesses = [(initial_fitness - min_fitness) / \
        (max_fitness - min_fitness) for initial_fitness in initial_fitnesses]
    final_fitnesses = [(final_fitness - min_fitness) / \
        (max_fitness - min_fitness) for final_fitness in final_fitnesses]

    fci = _FCI(initial_fitnesses, final_fitnesses)
    return fci


def _repaired_position(position, lower, upper):
    repaired_position = np.copy(position)
    for i in range(len(repaired_position)):
        repaired_position[i] = max(lower, min(upper, position[i]))
    return repaired_position


def _repaired_positions_and_indices(positions, lower, upper):
    repaired_positions = np.copy(positions)
    repaired_indices = []

    for i in range(len(repaired_positions)):
        repaired_positions[i] = _repaired_position(
            repaired_positions[i], lower, upper)
        if not np.array_equal(repaired_positions[i], positions[i]):
            repaired_indices.append(i)

    return (repaired_positions, repaired_indices)


def _FCI(initial_fitnesses, final_fitnesses):
    """
    Calculate the proportion of particles whose fitness have improved.
    """

    assert len(initial_fitnesses) == len(final_fitnesses), \
        'Cannot compute FCI. Initial and final fitnesses do not contain equal amounts of fitnesses.'

    # [initial_fitnesses, final_fitnesses].T is the fitness cloud.
    # The fitness cloud index is the proportion of fitnesses that improved.
    improvements = [1 if f_final < f_initial else 0
                    for f_final, f_initial in zip(final_fitnesses, initial_fitnesses)]
    num_improvements = np.sum(improvements)
    return float(num_improvements) / float(len(final_fitnesses))

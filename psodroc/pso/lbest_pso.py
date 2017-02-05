import numpy as np

# PSO parameters
w = None
c1 = None
c2 = None

# Swarm variables
swarm_size = 0
positions = None
velocities = None
fitnesses = None
pbest_positions = None # each particle's personal best
pbest_fitnesses = None
lbest_positions = None # each particle's local best
lbest_fitnesses = None

# Search space
function = None
num_dimensions = None
lower_bound = None # (same across all dimensions)
upper_bound = None


def init_swarm(size):
    # Initializes swarm with `size` number of particles.
    # Requires all search space parameters already to be set.
    _validate_search_space()

    global swarm_size
    swarm_size = size

    global positions
    positions = np.random.rand(swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound

    global fitnesses
    fitnesses = [function(position) for position in positions]

    global velocities
    velocities = np.random.rand(swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound

    global pbest_positions
    pbest_positions = np.copy(positions)

    global pbest_fitnesses
    pbest_fitnesses = [function(position) for position in pbest_positions]

    _update_lbests()


def init_pso_defaults():
    global w
    w =  0.729844
    global c1
    c1 = 1.49618
    global c2
    c2 = 1.49618


def iterate():
    # Performs one iteration of the algorithm.
    # Afterwards, the swarm's velocities, positions, fitnesses, personal best positions,
    # personal best fitnesses, and local best positions and fitnesses will be updated.
    # Requires the algorithm's and swarm's parameters to have been initialized.
    _validate_algorithm()
    _validate_swarm()

    global velocities
    global positions
    global fitnesses
    global pbest_positions
    global pbest_fitnesses
    global gbest_position

    inertia_component = w * velocities

    r1 = np.random.rand(swarm_size, num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions - positions)

    r2 = np.random.rand(swarm_size, num_dimensions)
    social_component = c2 * r2 * (lbest_positions - positions)

    unclamped_velocities = inertia_component + cognitive_component + social_component
    velocities = _clamped_velocities(unclamped_velocities)

    positions = positions + velocities

    fitnesses = [function(position) for position in positions]

    new_pbest_positions = []
    new_pbest_fitnesses = []
    for (old_pbest_position, old_pbest_fitness, current_position, current_fitness) in zip(pbest_positions, pbest_fitnesses, positions, fitnesses):
        if current_fitness < old_pbest_fitness:
            new_pbest_positions.append(current_position)
        else:
            new_pbest_positions.append(old_pbest_position)

    pbest_positions = new_pbest_positions

    pbest_fitnesses = [function(position) for position in pbest_positions]

    _update_lbests()


def _update_lbests():
    # Updates the lbest_positions and lbest_fitnesses of the swarm.
    # For each particle at index i, its neighbourhood consists of itself and the particles at indexes i-1 and i+1.
    # The lbest particle for each particle is the particle in its neighbourhood with the best fitness.
    _validate_search_space()

    global swarm_size
    global num_dimensions
    global lbest_positions
    global lbest_fitnesses
    lbest_positions = np.zeros((swarm_size, num_dimensions))
    lbest_fitnesses = np.zeros(swarm_size)
    for i in range(0, swarm_size):
        neighbour_indexes = _neighbourhood_indices_for_index(i)

        neighbour1_index = neighbour_indexes[0]
        neighbour1_position = positions[neighbour1_index]
        neighbour1_fitness = function(neighbour1_position)

        neighbour2_index = neighbour_indexes[1]
        neighbour2_position = positions[neighbour2_index]
        neighbour2_fitness = function(neighbour2_position)

        if neighbour1_fitness < fitnesses[i] or neighbour2_fitness < fitnesses[i]:
            if neighbour1_fitness < neighbour2_fitness:
                lbest_positions[i] = neighbour1_position
                lbest_fitnesses[i] = neighbour1_fitness
            else:
                lbest_positions[i] = neighbour2_position
                lbest_fitnesses[i] = neighbour2_fitness
        else:
            lbest_positions[i] = positions[i]
            lbest_fitnesses[i] = fitnesses[i]

def _neighbourhood_indices_for_index(i):
    # Returns the indices of the particles belonging to the neighbourhood of the particle at index i.
    # That is simply the particles at the index before and the index after i.
    neighbour1 = (i - 1 + swarm_size) % swarm_size
    neighbour2 = (i + 1) % swarm_size
    return [neighbour1, neighbour2]

def _clamped_velocities(unclamped_velocities):
    # Calculates and returns clamped velocities by performing `max(min(velocity, minimum_allowed), maximum_allowed)` on each velocity.
    clamp_min = np.full((swarm_size, num_dimensions), lower_bound)
    clamp_max = np.full((swarm_size, num_dimensions), upper_bound)
    velocities = np.maximum(np.minimum(unclamped_velocities, clamp_max), clamp_min)
    return velocities


_did_validate_search_space = False
def _validate_search_space():
    global _did_validate_search_space
    if _did_validate_search_space: # Only check once
        return
    if function is None:
        raise Exception("lbest_pso.function was not set")
    if num_dimensions is None:
        raise Exception("lbest_pso.num_dimensions was not set")
    if lower_bound is None:
        raise Exception("lbest_pso.lower_bound was not set")
    if upper_bound is None:
        raise Exception("lbest_pso.upper_bound was not set")
    _did_validate_search_space = True


_did_validate_algorithm = False
def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm:
        return
    if w is None:
        raise Exception("lbest_pso.w was not set")
    if c1 is None:
        raise Exception("lbest_pso.c1 was not set")
    if c2 is None:
        raise Exception("lbest_pso.c2 was not set")
    _did_validate_algorithm = True


_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm:
        return
    if positions is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if velocities is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if fitnesses is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if pbest_positions is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if pbest_fitnesses is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if lbest_positions is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if lbest_fitnesses is None:
        raise Exception("lbest_pso.init_swarm was not called")
    _did_validate_swarm = True

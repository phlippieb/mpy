import numpy as np

# PSO parameters
w = None # Inertia weight component
s = None # Successes threshhold
f = None # Failures threshhold

# Swarm variables
# TODO: validate all!
swarm_size = 0
positions = None
positions = None
velocities = None
fitnesses = None
pbest_positions = None
pbest_fitnesses = None
gbest_position = None
gbest_fitness = None
gbest_index = None
rho = 1.0
num_successes = 0
num_failures = 0

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

    gbest_index = np.argmin(pbest_fitnesses)
    global gbest_position
    gbest_position = np.copy(pbest_positions[gbest_index])

    global gbest_fitness
    gbest_fitness = function(gbest_position)

    global rho
    rho = 1.0

    global num_successes
    num_successes = 0

    global num_failures
    num_failures = 0

def init_pso_defaults():
    # Initializes the algorithm parameters `w`, `num_successes` and `num_failures` to commonly used default values.
    global w
    w =  0.729844
    global num_successes
    num_successes = 10 # TODO: what should this be? Find original GCPSO paper!
    global num_failures
    num_failures = 10 # TODO: what should this be?


def iterate():
    # Performs one iteration of the algorithm.
    # Afterwards, the swarm's velocities, positions, fitnesses, personal best positions,
    # personal best fitnesses, and global best positions and fitnesses will be updated.
    # Requires the algorithm's and swarm's parameters to have been initialized.
    _validate_algorithm()
    _validate_swarm()

    global velocities
    global positions
    global fitnesses
    global pbest_positions
    global pbest_fitnesses
    global gbest_position
    global rho
    global num_successes
    global num_failures

    inertia_component = w * velocities

    # Calculate new velocities, positions and fitnesses of each particle:
    for index in range(0, swarm_size):
        # TODO: if this is the best index
        _iterate_best(index)
        # TODO: else
        _iterate_non_best(index)

    # Update swarm gbest and pbests
    new_pbest_positions = []
    new_pbest_fitnesses = [] # TODO: use or remove!
    for (old_pbest_position, old_pbest_fitness, current_position, current_fitness) in zip(pbest_positions, pbest_fitnesses, positions, fitnesses):
        if current_fitness < old_pbest_fitness:
            new_pbest_positions.append(current_position)
        else:
            new_pbest_positions.append(old_pbest_position)

    pbest_positions = new_pbest_positions
    pbest_fitnesses = [function(position) for position in pbest_positions]

    gbest_index = np.argmin(pbest_fitnesses)
    gbest_position = pbest_positions[gbest_index]
    gbest_fitness = pbest_fitnesses[gbest_index]

def _iterate_best(index):
    # The swarm's best particle avoids premature convergence by performing a local search.
    # Param index: the index of the best particle.

    inertia_component = w * velocities[index]
    second_component = -(positions[index]) # TODO: is this part of the inertia comp? else, what should it be called?
    cognitive_component = pbest_positions[index] # TODO: this might be part of second_component?

    global rho
    if num_successes > s: # TODO: rename s => num_successes_threshhold or something; ditto for f
        rho = 2 * rho
    elif num_failures > f:
        rho = 0.5 * rho
    else:
        rho = rho # no-op

    r = np.rand(num_dimensions)
    search_component = r * rho

    unclamped_velocity = inertia_component + second_component + cognitive_component + search_component
    velocities[index] = _clamped_velocities(unclamped_velocity)

    positions[index] = positions[index] + velocities[index]

    # Determine whether this update results in a success or a failure.
    old_fitness = fitnesses[index]
    new_fitness = function(function(positions[index]))
    if new_fitness < old_fitness:
        num_failures = 0
        num_successes += 1
    elif new_fitness > old_fitness:
        num_successes = 0
        num_failures += 1

    fitnesses[index] = new_fitness

def _iterate_non_best(index):
    # Non-best particles are iterated like in a normal gbest PSO.
    # Param index: the index of the particle.

    inertia_component = w * velocities[index]

    r1 = np.random.rand(swarm_size, num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions[index] - positions[index])

    r2 = np.random.rand(swarm_size, num_dimensions)
    social_component = c2 * r2 * (gbest_position - positions[index])

    unclamped_velocity = inertia_component + cognitive_component + social_component
    velocities[index] = _clamped_velocities(unclamped_velocity)
    positions[index] = positions[index] + velocities[index]
    fitnesses[index] = [function(positions[index])]


    # TODO: test when given just one (should be fine, though?)
def _clamped_velocities(unclamped_velocities):
    # Returns the given velocities clamped between lower_bound and upper_bound.
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
        raise Exception("gc_gbest_pso.function was not set")
    if num_dimensions is None:
        raise Exception("gc_gbest_pso.num_dimensions was not set")
    if lower_bound is None:
        raise Exception("gc_gbest_pso.lower_bound was not set")
    if upper_bound is None:
        raise Exception("gc_gbest_pso.upper_bound was not set")
    _did_validate_search_space = True

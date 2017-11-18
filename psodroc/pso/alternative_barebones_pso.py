# Implemented as per
# https://pdfs.semanticscholar.org/8c38/4ec0ff05ace6326e366b131ee99d20bb1c6b.pdf
# TODO: source the original paper

import numpy as np

# Swarm variables
swarm_size = 0
positions = None
fitnesses = None
pbest_positions = None # each particle's personal best
pbest_fitnesses = None
lbest_positions = None # each particle's local best
lbest_fitnesses = None
gbest_position = None # the swarm's global best; not used in the algorithm, but exposed as a metric
gbest_fitness = None

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

    global pbest_positions
    pbest_positions = np.copy(positions)

    global pbest_fitnesses
    pbest_fitnesses = [function(position) for position in pbest_positions]

    global gbest_position
    global gbest_fitness
    gbest_index = np.argmin(pbest_fitnesses)
    gbest_position = pbest_positions[gbest_index]
    gbest_fitness = pbest_fitnesses[gbest_index]

def init_pso_defaults():
    # Nothing to init
    return

def iterate():
    # Performs one iteration of the algorithm.
    # Afterwards, the swarm's velocities, positions, fitnesses, personal best positions,
    # personal best fitnesses, and local best positions and fitnesses will be updated.
    # Requires the algorithm's and swarm's parameters to have been initialized.
    _validate_swarm()

    global velocities
    global positions
    global fitnesses
    global pbest_positions
    global pbest_fitnesses
    global gbest_position
    global gbest_fitness

    # Update each particle's velocity using the current personal and global best positions.
    velocities = [_velocity(pbest_position, gbest_position) for pbest_position in pbest_positions]

    # Update each particle's position to its velocity.
    # TODO: is this correct?
    positions = velocities

    # Update fitnesses from positions.
    fitnesses = [function(position) for position in positions]

    # Update the personal global best positions and fitnesses.
    new_pbest_positions = []
    new_pbest_fitnesses = []
    for (old_pbest_position, old_pbest_fitness, current_position, current_fitness) in zip(pbest_positions, pbest_fitnesses, positions, fitnesses):
        if current_fitness < old_pbest_fitness:
            new_pbest_positions.append(current_position)
        else:
            new_pbest_positions.append(old_pbest_position)

    pbest_positions = new_pbest_positions
    pbest_fitnesses = [function(pbest_position) for pbest_position in pbest_positions]

    gbest_index = np.argmin(pbest_fitnesses)
    gbest_position = pbest_positions[gbest_index]
    gbest_fitness = pbest_fitnesses[gbest_index]

def _velocity(pbest_position, gbest_position):
    # In Alternative Barebones PSO, the velocity of a particle is a vector sampled from a Gaussian distribution with its mean between the particle's pbest and gbest positions, and with a deviation of the distance between those two points.
    # The velocity is also recombined with the particle's personal best position; at each dimension, the position is replaced with the personal best position (for that dimension) at a 0.5 propability.
    # This returns such a vector.

    # If pbest == gbest, the attractor point is simply that point.
    if np.array_equal(pbest_position, gbest_position):
        return pbest_position

    mean = (pbest_position + gbest_position) / 2
    deviation = np.abs(pbest_position - gbest_position)

    velocity = _gaussian(mean, deviation)
    velocity = _recombine(velocity, pbest_position)
    return velocity

def _gaussian(mean, deviation):
    # Numpy's random.normal expects deviation to be > 0 in every dimension.
    # This sidesteps that by just using the mean in any dimension where the deviation is zero.
    result = mean
    i = 0
    for (mean_i, deviation_i) in zip(mean, deviation):
        if deviation_i > 0:
            velocity_i = np.random.normal(mean_i, deviation_i)
            result[i] = velocity_i
        i += 1
    return result

def _recombine(velocity, pbest_position):
    result = velocity
    for i in range(0, velocity.size):
        if np.random.uniform(0, 1) < 0.5:
            # Recombine this dimension with the personal best position.
            result[i] = pbest_position[i]
    return result

_did_validate_search_space = False
def _validate_search_space():
    global _did_validate_search_space
    if _did_validate_search_space: return

    assert function is not None, "gbest_pso.function was not set"
    assert num_dimensions is not None, "gbest_pso.num_dimensions was not set"
    assert lower_bound is not None, "gbest_pso.lower_bound was not set"
    assert upper_bound is not None, "gbest_pso.upper_bound was not set"
    _did_validate_search_space = True

_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm: return

    assert positions is not None, "gbest_pso.init_swarm was not called"
    assert fitnesses is not None, "gbest_pso.init_swarm was not called"
    assert pbest_positions is not None, "gbest_pso.init_swarm was not called"
    assert pbest_fitnesses is not None, "gbest_pso.init_swarm was not called"
    assert gbest_position is not None, "gbest_pso.init_swarm was not called"
    assert gbest_fitness is not None, "gbest_pso.init_swarm was not called"
    _did_validate_swarm = True

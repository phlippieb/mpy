import numpy as np

# PSO parameters
w = None # inertia component weight
c1 = None # social component constant

# Swarm variables
swarm_size = 0
positions = None
velocities = None
fitnesses = None
gbest_position = None
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

    global velocities
    velocities = np.random.rand(swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound

    # Personal bests aren't used to guide the swarm,
    # but they are used here as a convenience to find the global best.
    pbest_positions = np.copy(positions)
    pbest_fitnesses = [function(position) for position in pbest_positions]
    gbest_index = np.argmin(pbest_fitnesses)

    global gbest_position
    gbest_position = np.copy(pbest_positions[gbest_index])

    global gbest_fitness
    gbest_fitness = function(gbest_position)


def init_pso_defaults():
    # Initializes the algorithm parameters `w` and `c1` to commonly used default values.
    global w
    w =  0.729844
    global c1
    c1 = 1.49618

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
    global gbest_position

    inertia_component = w * velocities

    r1 = np.random.rand(swarm_size, num_dimensions)
    social_component = c1 * r1 * (gbest_position - positions)

    unclamped_velocities = inertia_component + social_component
    velocities = _clamped_velocities(unclamped_velocities)

    positions = positions + velocities

    fitnesses = [function(position) for position in positions]

    gbest_index = np.argmin(fitnesses)
    gbest_position = positions[gbest_index]
    gbest_fitness = fitnesses[gbest_index]


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
        raise Exception("gbest_pso.function was not set")
    if num_dimensions is None:
        raise Exception("gbest_pso.num_dimensions was not set")
    if lower_bound is None:
        raise Exception("gbest_pso.lower_bound was not set")
    if upper_bound is None:
        raise Exception("gbest_pso.upper_bound was not set")
    _did_validate_search_space = True

_did_validate_algorithm = False
def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm:
        return
    if w is None:
        raise Exception("gbest_pso.w was not set")
    if c1 is None:
        raise Exception("gbest_pso.c1 was not set")
    _did_validate_algorithm = True

_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm:
        return
    if positions is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if velocities is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if fitnesses is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if gbest_position is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if gbest_fitness is None:
        raise Exception("gbest_pso.init_swarm was not called")
    _did_validate_swarm = True

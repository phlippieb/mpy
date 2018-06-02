import numpy as np

# PSO parameters
w = None  # inertia component weight
c2 = None  # social component constant

# Swarm variables
swarm_size = 0
positions = None
velocities = None
fitnesses = None
pbest_positions = None
pbest_fitnesses = None

# Search space
function = None
num_dimensions = None
lower_bound = None  # (same across all dimensions)
upper_bound = None


# Initialization


def init_search_space(function, num_dimensions, lower_bound, upper_bound):
    # Initializes the swarm size with all required parameters.

    globals().update(function=function, num_dimensions=num_dimensions,
                     lower_bound=lower_bound, upper_bound=upper_bound)


def init_swarm(size):
    # Initializes swarm with `size` number of particles.
    # Requires all search space parameters already to be set.
    _validate_search_space()

    global swarm_size
    swarm_size = size

    global positions
    positions = np.random.rand(
        swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound

    global fitnesses
    fitnesses = [function(position) for position in positions]

    global velocities
    velocities = np.zeros([swarm_size, num_dimensions])

    global pbest_positions
    pbest_positions = np.copy(positions)

    global pbest_fitnesses
    pbest_fitnesses = [function(position) for position in pbest_positions]


def init_pso_defaults():
    # Initializes the algorithm parameters `w` and `c1` to commonly used default values.
    global w
    w = 0.729844
    global c2
    c2 = 1.49618


# Iteration


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

    inertia_component = w * velocities

    r2 = np.random.rand(swarm_size, num_dimensions)
    cognitive_component = c2 * r2 * (pbest_positions - positions)

    velocities = inertia_component + cognitive_component

    positions = positions + velocities

    fitnesses = [function(position) for position in positions]

    for i in range(swarm_size):
        # Update the pbest position and fitness for particle i if it is still valid.
        if _position_is_within_bounds(positions[i]) and fitnesses[i] < pbest_fitnesses[i]:
            pbest_positions[i] = positions[i]
            pbest_fitnesses[i] = fitnesses[i]


def _position_is_within_bounds(position):
    # A position is considered to be within the bounds of the search space only if
    # each dimension component is within those bounds.
    for position_j in position:
        if position_j < lower_bound or position_j > upper_bound:
            return False
    return True


# Validation


_did_validate_search_space = False


def _validate_search_space():
    global _did_validate_search_space
    if _did_validate_search_space:
        return

    assert function is not None, "cognitive_only_pso.function was not set"
    assert num_dimensions is not None, "cognitive_only_pso.num_dimensions was not set"
    assert lower_bound is not None, "cognitive_only_pso.lower_bound was not set"
    assert upper_bound is not None, "cognitive_only_pso.upper_bound was not set"
    _did_validate_search_space = True


_did_validate_algorithm = False


def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm:
        return

    assert w is not None, "cognitive_only_pso.w was not set"
    assert c2 is not None, "cognitive_only_pso.c1 was not set"
    _did_validate_algorithm = True


_did_validate_swarm = False


def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm:
        return

    error_message = 'cognitive_only_pso.init_swarm was not called'
    assert positions is not None, error_message
    assert velocities is not None, error_message
    assert fitnesses is not None, error_message
    assert pbest_positions is not None, error_message
    assert pbest_fitnesses is not None, error_message
    _did_validate_swarm = True

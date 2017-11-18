import numpy as np

# PSO parameters
w = None # inertia component weight
c1 = None # cognitive component constant
c2 = None # social component constant

# Swarm variables
swarm_size = 0
positions = None
velocities = None
fitnesses = None
pbest_positions = None
pbest_fitnesses = None
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

    global pbest_positions
    pbest_positions = np.copy(positions)

    global pbest_fitnesses
    pbest_fitnesses = [function(position) for position in pbest_positions]

    gbest_index = np.argmin(pbest_fitnesses)
    global gbest_position
    gbest_position = np.copy(pbest_positions[gbest_index])

    global gbest_fitness
    gbest_fitness = function(gbest_position)


def init_pso_defaults():
    # Initializes the algorithm parameters `w`, `c1` and `c2` to commonly used default values.
    global w
    w =  0.729844
    global c1
    c1 = 1.49618
    global c2
    c2 = 1.49618


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
    global gbest_fitness

    inertia_component = w * velocities

    r1 = np.random.rand(swarm_size, num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions - positions)

    r2 = np.random.rand(swarm_size, num_dimensions)
    social_component = c2 * r2 * (gbest_position - positions)

    velocities = inertia_component + cognitive_component + social_component

    positions = positions + velocities

    fitnesses = [function(position) for position in positions]

    new_pbest_positions = []
    for (old_pbest_position, old_pbest_fitness, current_position, current_fitness) in zip(pbest_positions, pbest_fitnesses, positions, fitnesses):
        if current_fitness < old_pbest_fitness and _position_is_within_bounds(current_position):
            new_pbest_positions.append(current_position)
        else:
            new_pbest_positions.append(old_pbest_position)

    pbest_positions = new_pbest_positions
    pbest_fitnesses = [function(position) for position in pbest_positions]

    gbest_index = np.argmin(pbest_fitnesses)
    gbest_position = pbest_positions[gbest_index]
    gbest_fitness = pbest_fitnesses[gbest_index]

def _position_is_within_bounds(position):
    # A position is considered to be within the bounds of the search space only if
    # each dimension component is within those bounds.
    for position_j in position:
        if position_j < lower_bound or position_j > upper_bound:
            return False
    return True

_did_validate_search_space = False
def _validate_search_space():
    global _did_validate_search_space
    if _did_validate_search_space: return

    assert function is not None, "gbest_pso.function was not set"
    assert num_dimensions is not None, "gbest_pso.num_dimensions was not set"
    assert lower_bound is not None, "gbest_pso.lower_bound was not set"
    assert upper_bound is not None, "gbest_pso.upper_bound was not set"
    _did_validate_search_space = True

_did_validate_algorithm = False
def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm: return

    assert w is not None, "gbest_pso.w was not set"
    assert c1 is not None, "gbest_pso.c1 was not set"
    assert c2 is not None, "gbest_pso.c2 was not set"
    _did_validate_algorithm = True

_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm: return

    assert positions is not None, "gbest_pso.init_swarm was not called"
    assert velocities is not None, "gbest_pso.init_swarm was not called"
    assert fitnesses is not None, "gbest_pso.init_swarm was not called"
    assert pbest_positions is not None, "gbest_pso.init_swarm was not called"
    assert pbest_fitnesses is not None, "gbest_pso.init_swarm was not called"
    assert gbest_position is not None, "gbest_pso.init_swarm was not called"
    assert gbest_fitness is not None, "gbest_pso.init_swarm was not called"
    _did_validate_swarm = True

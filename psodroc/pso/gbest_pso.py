import numpy as np

# PSO parameters
# Init these
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
# Init these
function = None
num_dimensions = None
lower_bound = None # (same across all dimensions)
upper_bound = None


def init_swarm(size):
    _check_search_space_vars()

    global swarm_size
    swarm_size = size

    global positions
    positions = np.random.rand(swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound

    global fitnesses
    fitnesses = [function(position) for position in positions]

    global velocities
     # TODO should this be randomly initialized? check lit
    velocities = np.zeros([swarm_size, num_dimensions])

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
    global w
    w =  0.729844
    global c1
    c1 = 1.49618
    global c2
    c2 = 1.49618


def iterate():
    _check_pso_vars()
    _check_swarm()

    global velocities
    global positions
    global fitnesses
    global pbest_positions
    global pbest_fitnesses
    global gbest_position

    inertia_component = w * velocities

    r1 = np.random.rand(swarm_size, num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions - positions)
    df = positions - pbest_positions

    r2 = np.random.rand(swarm_size, num_dimensions)
    social_component = c2 * r2 * (gbest_position - positions)

    unclamped_velocities = inertia_component + cognitive_component + social_component
    velocities = _clamp_velocities(unclamped_velocities)

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

    gbest_index = np.argmin(pbest_fitnesses)
    gbest_position = pbest_positions[gbest_index]
    gbest_fitness = pbest_fitnesses[gbest_index]

def _clamp_velocities(unclamped_velocities):
    clamp_min = np.full((swarm_size, num_dimensions), lower_bound)
    clamp_max = np.full((swarm_size, num_dimensions), upper_bound)
    velocities = np.maximum(np.minimum(unclamped_velocities, clamp_max), clamp_min)
    return velocities

def _check_search_space_vars():
    if function is None:
        raise Exception("gbest_pso.function was not set")
    if num_dimensions is None:
        raise Exception("gbest_pso.num_dimensions was not set")
    if lower_bound is None:
        raise Exception("gbest_pso.lower_bound was not set")
    if upper_bound is None:
        raise Exception("gbest_pso.upper_bound was not set")

def _check_pso_vars():
    if w is None:
        raise Exception("gbest_pso.w was not set")
    if c1 is None:
        raise Exception("gbest_pso.c1 was not set")
    if c2 is None:
        raise Exception("gbest_pso.c2 was not set")

def _check_swarm():
    if positions is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if velocities is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if fitnesses is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if pbest_positions is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if pbest_fitnesses is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if gbest_position is None:
        raise Exception("gbest_pso.init_swarm was not called")
    if gbest_fitness is None:
        raise Exception("gbest_pso.init_swarm was not called")

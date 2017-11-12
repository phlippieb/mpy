import numpy as np

# PSO parameters
w = None # Inertia weight component
c1 = None # Cognitive component constant
c2 = None # Social component constant
s = None # Successes threshhold -- same for each neighbourhood
f = None # Failures threshhold -- same for each neighbourhood

# Swarm variables
swarm_size = None # The number of particles in the swarm
positions = None # An array of position vectors (one for each particle)
velocities = None # An array of velocity values (one for each particle)
fitnesses = None # An array of fitness values in terms of the objective function (one for each particle)
pbest_positions = None # An array of vectors, each giving the position of a particle's best position so far
pbest_fitnesses = None # An array of values, each giving the fitness of a particle's best position so far
lbest_indices = None # An array of indices identifying the best particle in each particle's neighbourhood
lbest_positions = None # An array of vectors, each giving the position of the best position found in a particle's neighbourhood so far
lbest_fitnesses = None # An array of values, each giving the best fitness found in a particle's neighbourhood so far
rhos = None # A rho value for each neighbourhood; used when updating the neighbourhood's best particle
nums_successes = None # The number of successes of the best particle of each neighbourhood
nums_failures = None # The number of failures of the best particle of each neighbourhood

# Search space parameters
function = None # The objective function to minimize
num_dimensions = None # The number of dimensions of the objective function; thus, the size of each particle's position vector
lower_bound = None # The domain bounds of the search space; same across all dimensions
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

    global lbest_indices
    lbest_indices = np.zeros(swarm_size)

    global lbest_positions
    lbest_positions = np.zeros((swarm_size, num_dimensions))

    global lbest_fitnesses
    lbest_fitnesses = np.zeros(swarm_size)

    _update_lbests()

    global rhos
    rhos = np.full(size, 1.)

    global nums_successes
    nums_successes = np.full(size, 0)

    global nums_failures
    nums_failures = np.full(size, 0)

def init_pso_defaults():
    # Initializes the algorithm parameters `w`, `f` and `s` to commonly used default values.
    global w
    w =  0.729844
    global c1
    c1 = 1.49618
    global c2
    c2 = 1.49618
    global f
    f = 5
    global s
    s = 15

def iterate():
    # Update each particle. Each neighbourhood's best particle is updated according to a different equation.
    # Requires initialized algorithm and swarm parameters.
    _validate_algorithm()
    _validate_swarm()

    for index in range(0, swarm_size):
        if index in lbest_indices:
            _iterate_best(index)
        else:
            _iterate_non_best(index)

    # All particles are updated. Determine the neighbourhood-best values.
    _update_lbests()

def _neighbourhood_indices_for_index(i):
    # Returns the indices of the particles belonging to the neighbourhood of the particle at index i.
    # That is simply the particles at the index before and the index after i.
    neighbour1 = (i - 1 + swarm_size) % swarm_size
    neighbour2 = (i + 1) % swarm_size
    return [neighbour1, neighbour2]

def _update_lbests():
    # Updates the lbest_indices, lbest_positions and lbest_fitnesses of the swarm.
    # For each particle at index i, its neighbourhood consists of itself and the particles at indexes i-1 and i+1.
    # The lbest particle for each particle is the one the best pbest in its neighbourhood.
    _validate_search_space()

    global swarm_size
    global num_dimensions
    global lbest_indices
    global lbest_positions
    global lbest_fitnesses

    for i in range(0, swarm_size):
        neighbour_indexes = _neighbourhood_indices_for_index(i)
        neighbour1_index = neighbour_indexes[0] # i-1 % swarm_size
        neighbour2_index = neighbour_indexes[1] # i+1 % swarm_size

        # Find the particle in the neighbourhood with the best pbest.
        # (This is only an index within this particle's neighbourhood)
        best = np.argmin([
            pbest_fitnesses[i], # 0
            pbest_fitnesses[neighbour1_index], # 1
            pbest_fitnesses[neighbour2_index], # 2
        ])

        lbest_index = None
        if best == 0:
            lbest_index = i
        elif best == 1:
            lbest_index = neighbour1_index
        else:
            lbest_index = neighbour2_index

        lbest_indices[i] = lbest_index
        lbest_positions[i] = pbest_positions[lbest_index]
        lbest_fitnesses[i] = pbest_fitnesses[lbest_index]

def _iterate_best(index):
    # Perofrms a special iteration of the algorithm for neighbourhood's most fit particle, identified by the given index.
    # Afterwards, the velocity, position, fitness, personal best position and personal best fitness
    # of the best particle, as well as rho, nums_successes and nums_failures for each neighbourhood will be updated.

    global velocities
    global positions
    global fitnesses
    global pbest_fitnesses
    global pbest_positions
    global nums_successes
    global nums_failures
    global rhos

    inertia_component = w * velocities[index]

    r2 = np.random.rand(num_dimensions)
    local_search_component = rhos[index] * (1 - (2 * r2))

    unclamped_velocity = -(positions[index]) + lbest_positions[index] + inertia_component + local_search_component
    velocity = _clamp_velocity(unclamped_velocity)

    position = lbest_positions[index] + inertia_component + local_search_component

    fitness = function(position)

    velocities[index] = velocity

    positions[index] = position

    fitnesses[index] = fitness


    if fitness < pbest_fitnesses[index]:
        pbest_fitnesses[index] = fitness
        pbest_positions[index] = position
        nums_successes[index] += 1
        nums_failures[index] = 0
    else:
        nums_failures[index] += 1
        nums_successes[index] = 0

    if nums_successes[index] > s:
        rhos[index] *= 2.
    elif nums_failures[index] > f:
        # Here we do rho /= 2, but ensure that rho never reaches zero.
        rho = rhos[index] / 2
        rhos[index] = max(rho, np.finfo(float).tiny)
    # Else, rho remains the same.

def _iterate_non_best(index):
    # Performs a normal iteration of the algorithm for the single particle identified by the given index.
    # Afterwards, the velocity, position, fitness, personal best position, and personal best fitness
    # will be updated for this particle -- i.e. at the given index of the respective arrays.
    global velocities
    global positions
    global fitnesses
    global pbest_fitnesses
    global pbest_positions

    inertia_component = w * velocities[index]

    r1 = np.random.rand(num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions[index] - positions[index])

    r2 = np.random.rand(num_dimensions)
    social_component = c2 * r2 * (lbest_positions[index] - positions[index])

    unclamped_velocity = inertia_component + cognitive_component + social_component
    velocity = _clamp_velocity(unclamped_velocity)

    position = positions[index] + velocity

    fitness = function(position)

    velocities[index] = velocity

    positions[index] = position

    fitnesses[index] = fitness

    if fitness < pbest_fitnesses[index]:
        pbest_fitnesses[index] = fitness
        pbest_positions[index] = position

def _clamp_velocity(unclamped_velocity):
    # Returns the given velocity clamped between lower_bound and upper_bound.
    velocity = np.maximum(np.minimum(unclamped_velocity, upper_bound), lower_bound)
    return velocity

# Validation

_did_validate_search_space = False
def _validate_search_space():
    global _did_validate_search_space
    if _did_validate_search_space: return

    assert function is not None, "gc_lbest_pso.function was not set"
    assert num_dimensions is not None, "gc_lbest_pso.num_dimensions was not set"
    assert lower_bound is not None, "gc_lbest_pso.lower_bound was not set"
    assert upper_bound is not None, "gc_lbest_pso.upper_bound was not set"
    _did_validate_search_space = True

_did_validate_algorithm = False
def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm: return

    assert w is not None, "gc_lbest_pso.w was not set"
    assert c1 is not None, "gc_lbest_pso.c1 was not set"
    assert c2 is not None, "gc_lbest_pso.c2 was not set"
    assert s is not None, "gc_lbest_pso.s was not set"
    assert f is not None, "gc_lbest_pso.f was not set"
    _did_validate_algorithm = True

_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm: return

    assert swarm_size is not None, "gc_lbest_pso.init_swarm was not called"
    assert positions is not None, "gc_lbest_pso.init_swarm was not called"
    assert velocities is not None, "gc_lbest_pso.init_swarm was not called"
    assert fitnesses is not None, "gc_lbest_pso.init_swarm was not called"
    assert pbest_positions is not None, "gc_lbest_pso.init_swarm was not called"
    assert pbest_fitnesses is not None, "gc_lbest_pso.init_swarm was not called"
    assert lbest_indices is not None, "gc_lbest_pso.init_swarm was not called"
    assert lbest_positions is not None, "gc_lbest_pso.init_swarm was not called"
    assert lbest_fitnesses is not None, "gc_lbest_pso.init_swarm was not called"
    assert rhos is not None, "gc_lbest_pso.init_swarm was not called"
    assert nums_successes is not None, "gc_lbest_pso.init_swarm was not called"
    assert nums_failures is not None, "gc_lbest_pso.init_swarm was not called"

    _did_validate_swarm = True

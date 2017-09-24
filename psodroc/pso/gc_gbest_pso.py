import numpy as np

# PSO parameters
w = None # Inertia weight component
c1 = None # cognitive component constant
c2 = None # social component constant
s = None # Successes threshhold
f = None # Failures threshhold

# Swarm variables
swarm_size = None
positions = None
velocities = None
fitnesses = None
pbest_positions = None
pbest_fitnesses = None
gbest_position = None
gbest_fitness = None
gbest_index = None
rho = 1.
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

    global gbest_index
    gbest_index = np.argmin(pbest_fitnesses)
    
    global gbest_position
    gbest_position = np.copy(pbest_positions[gbest_index])

    global gbest_fitness
    gbest_fitness = function(gbest_position)

    global rho
    rho = 1.

    global num_successes
    num_successes = 0

    global num_failures
    num_failures = 0

def init_pso_defaults():
    # Initializes the algorithm parameters `w`, `num_successes` and `num_failures` to commonly used default values.
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
    # Update each particle. The swarm's most fit particle is updated according to a different formula.
    # Requires initialized algorithm and swarm parameters.
    _validate_algorithm()
    _validate_swarm()
    
    global gbest_index
    global gbest_position
    global gbest_fitness
    
    for index in range(0, swarm_size):
        if index == gbest_index:
            _iterate_best()
        else:
            _iterate_non_best(index)
    
    # All particles are updated; now just determine the global best values.
    new_gbest_index = np.argmin(pbest_fitnesses)
    if gbest_index != new_gbest_index:
        gbest_index = new_gbest_index
        num_successes = 0
        num_failures = 0
        # rho remains unchanged
    
    gbest_position = pbest_positions[gbest_index]
    
    gbest_fitness = pbest_fitnesses[gbest_index]

def _iterate_best():
    # Perofrms a special iteration of the algorithm for the swarm's most fit particle.
    # Afterwards, the velocity, position, fitness, personal best position and personal best fitness
    # of the best particle, as well as rho, num_successes and num_failures will be updated.
    
    global velocities
    global rho
    global positions
    global fitnesses
    global pbest_fitnesses
    global pbest_positions
    global num_successes
    global num_failures
    
    inertia_component = w * velocities[gbest_index]
    
    r2 = np.random.rand(num_dimensions)
    local_search_component = rho * (1 - (2 * r2))
    
    unclamped_velocity = -(positions[gbest_index]) + gbest_position + inertia_component + local_search_component
    velocity = _clamp_velocity(unclamped_velocity)
    
    position = gbest_position + inertia_component + local_search_component
    # i.e. positions[gbest_index] + velocity
    
    fitness = function(position)
    
    velocities[gbest_index] = velocity
    
    positions[gbest_index] = position
    
    fitnesses[gbest_index] = fitness
    
    if fitness < pbest_fitnesses[gbest_index]:
        pbest_fitnesses[gbest_index] = fitness
        pbest_positions[gbest_index] = position
        num_successes += 1
        num_failures = 0
    else:
        num_failures += 1
        num_successes = 0
    
    if num_successes > s:
        rho *= 2.
    elif num_failures > f:
        # Here we do rho /= 2, but ensure that rho never reaches zero.
        rho = max(rho / 2, np.finfo(float).tiny)
    # Else, rho remains the same.
        
def _iterate_non_best(index):
    # Performs a normal iteration of the algorithm for the single particle identified by the given index.
    # Afterwards, the velocity, position, fitness, personal best position, and personal best fitness
    # will be updated for this particle -- i.e. at the given index of the respective arrays.
    global velocities
    global positions
    global pbest_positions
    global fitnesses
    global pbest_fitnesses
    
    inertia_component = w * velocities[index]
    
    r1 = np.random.rand(num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions[index] - positions[index])
    
    r2 = np.random.rand(num_dimensions)
    social_component = c2 * r2 * (gbest_position - positions[index])
    
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

    assert function is not None, "gc_gbest_pso.function was not set"
    assert num_dimensions is not None, "gc_gbest_pso.num_dimensions was not set"
    assert lower_bound is not None, "gc_gbest_pso.lower_bound was not set"
    assert upper_bound is not None, "gc_gbest_pso.upper_bound was not set"
    _did_validate_search_space = True

_did_validate_algorithm = False
def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm: return

    assert w is not None, "gc_gbest_pso.w was not set"
    assert c1 is not None, "gc_gbest_pso.c1 was not set"
    assert c2 is not None, "gc_gbest_pso.c2 was not set"
    assert s is not None, "gc_gbest_pso.s was not set"
    assert f is not None, "gc_gbest_pso.f was not set"
    _did_validate_algorithm = True

_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm: return
   
    assert swarm_size is not None, "gc_gbest_pso.init_swarm was not called" 
    assert positions is not None, "gc_gbest_pso.init_swarm was not called"
    assert velocities is not None, "gc_gbest_pso.init_swarm was not called"
    assert fitnesses is not None, "gc_gbest_pso.init_swarm was not called"
    assert pbest_positions is not None, "gc_gbest_pso.init_swarm was not called"
    assert pbest_fitnesses is not None, "gc_gbest_pso.init_swarm was not called"
    assert gbest_position is not None, "gc_gbest_pso.init_swarm was not called"
    assert gbest_fitness is not None, "gc_gbest_pso.init_swarm was not called"
    assert gbest_index is not None, "gc_gbest_pso.init_swarm was not called"
    _did_validate_swarm = True

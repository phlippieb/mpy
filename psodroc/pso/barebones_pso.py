import numpy as np

# Swarm variables
swarm_size = 0
positions = None
fitnesses = None
pbest_positions = None # Each particle's personal best
pbest_fitnesses = None
gbest_position = None # The swarm's personal best
gbest_fitnesse = None

# Search space
function = None
num_dimensions = None
lower_bound = None # Same in all dimensions
upper_bound = None


def init_swarm(size):
    # Initialize a swarm with `size` particles.
    # Requires all search space parameters to be set.
    _validate_search_space()
    
    global swarm_size
    swarm_size = size
    
    # The swarm positions are initialized randomly across the search space.
    global positions
    positions = np.random.rand(swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound
    
    # The current fitnesses are determined for each particle's position.
    global fitnesses
    fitnesses = [function(position) for position in positions]
    
    # Each particle's initial personal best position is its current position.
    global pbest_positions
    pbest_positions = np.copy(positions)
    
    # Each particle's initial personal best fitness is its current fitness.
    global pbest_fitnesses
    pbest_fitnesses = np.copy(fitnesses)
    
    # The fittest particle is determined, and is used as the swarm's gbest.
    gbest_index = np.argmin(pbest_fitnesses)
    
    global gbest_position
    gbest_position = pbest_positions[gbest_index]
    
    global gbest_fitness
    gbest_fitness = pbest_fitnesses[gbest_index]
    
def init_pso_defaults():
    # Nothing to init.
    pass
    

def iterate():
    # Performs one iteration of the algorithm.
    # Afterwards, the swarm's velocities, positions, fitnesses, personal best positions,
    # personal best fitnesses, and global best position and fitness will be updated.
    # Requires the algorithm's and swarm's parameters to have been initialized.
    _validate_swarm()
    
    # Each particle's position is sampled around a theoretical attraction point
    # between its personal and global best.
    global positions
    positions = [_updated_position(i) for i in range(swarm_size)]
    
    # Update each particle's fitness at its new position.
    global fitnesses
    fitnesses = [function(position) for position in positions]
    
    # Update each particle's pbest.
    global pbest_positions
    global pbest_fitnesses
    pbests_changed = False
    for i in range(swarm_size):
        if fitnesses[i] <= pbest_fitnesses[i] and _position_is_within_bounds(positions[i]):
            pbest_positions[i] = positions[i]
            pbest_fitnesses[i] = fitnesses[i]
            pbests_changed = True
    
    # Update the swarm's gbest.
    if pbests_changed:
        gbest_index = np.argmin(pbest_fitnesses)
        global gbest_position
        gbest_position = pbest_positions[gbest_index]
        global gbest_fitness
        gbest_fitness = pbest_fitnesses[gbest_index]
            
def _updated_position(i):
    # Sample and return a new position for particle i.
    pbest_position = pbest_positions[i]
    
    # The new position is sampled from a normal (Gaussian) distribution.
    # The deviation of the distribution is determined per dimension:
    return [_updated_position_component(pbest_position_component, gbest_position_component) \
        for pbest_position_component, gbest_position_component in zip(pbest_position, gbest_position)]

def _updated_position_component(pbest_position_component, gbest_position_component):
    # Sample and return a new value for a dimensional component of a particle's position.
    # The position component is sampled from a normal (Gaussian) distribution.
    # The deviation of the distribution is the absolute difference between the position components.
    # If the pbest and gbest components coincide, and the distribution deviation is zero, no sampling is required (or possible).
    if pbest_position_component == gbest_position_component:
        return pbest_position_component
    else:
        distribution_deviation = abs(pbest_position_component - gbest_position_component)
    
    # The mean of the distribution is the mean of the two components.
    distribution_mean = (pbest_position_component + gbest_position_component) / 2
    
    # Sample and return.
    return np.random.normal(distribution_mean, distribution_deviation)
    
def _position_is_within_bounds(position):
    for position_j in position:
        if position_j < lower_bound or position_j > upper_bound:
            return False
    return True
    
# Validation:

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
    
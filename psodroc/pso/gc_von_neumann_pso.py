import numpy as np
import warnings

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
gbest_fitness = None # The best fitness among the swarm's lbest fitnesses; not used in the algorithm, but exposed as a metric
rhos = None # An array containing a rho value for each neighbourhood; used when updating the neighbourhood's best particle
nums_successes = None # An array containing the number of successes of the best particle of each neighbourhood
nums_failures = None # An array containing the number of failures of the best particle of each neighbourhood

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
    # TODO: this is wrong; fix everywhere!
    velocities = np.random.rand(swarm_size, num_dimensions) * (upper_bound - lower_bound) + lower_bound

    # Each particle's best position at first is simply its initial position.
    global pbest_positions
    pbest_positions = np.copy(positions)

    # Each particle's best fitness at first is simply its initial fitness,
    # which is its initial position evaluated by the objective function.
    global pbest_fitnesses
    pbest_fitnesses = [function(position) for position in pbest_positions]

    _init_grid()

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
    # Initializes the algorithm parameters `w`, 'c1', 'c2', `f` and `s` to commonly used default values.
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
    # Update each particle. Each neighbourhood's best particle is updated according to a special equation.
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

_grid = None
_grid_rows = None
_grid_cols = None
def _init_grid():
    # _grid is a 2D grid containing indices of particles.
    # It is used to determine the indices of a particle's Von Neumann neighbours.
    # We use the smallest square that can contain an index for every particle, fill it row-by-row, and trim empty rows.
    # Empty cells are set to -1.
    global _grid
    global _grid_rows
    global _grid_cols

    # How many columns does the smallest necessary square have?
    _grid_cols = _side_of_smallest_square_containing(swarm_size)
    # How many rows are filled, given the grids columns?
    _grid_rows = _rows_of_square_filled(_grid_cols, swarm_size)

    # Fill with -1 to indicate empty cells.
    _grid = np.full((_grid_rows, _grid_cols), -1, dtype=np.int64)

    # Iterate over grid and fill with swarm indices.
    index = 0
    for row in range(0, _grid_rows):
        for col in range(0, _grid_cols):
            if index < swarm_size:
                _grid[row, col] = index
                index += 1
            else:
                # All swarm indices are accounted for; return, leaving rest of grid with -1s.
                return

def _update_lbests():
    # Updates the lbest_positions and lbest_fitnesses of the swarm.
    # Each particle's neighbourhood consists of the particles adjacent to it on a 2D grid.
    # The local best particle in each neighbourhood is the particle with best pbest.
    _validate_search_space()

    global swarm_size
    global num_dimensions
    global lbest_positions
    global lbest_fitnesses

    for i in range(0, swarm_size):
        neighbour_above_index = _index_above(i)
        neighbour_left_index = _index_left_of(i)
        neighbour_right_index = _index_right_of(i)
        neighbour_below_index = _index_below(i)

        # Find the particle in the neighbourhood with the best pbest:
        # (This is only an index with this particle's neighbourhood)
        best = np.argmin([
            pbest_fitnesses[i], # 0
            pbest_fitnesses[neighbour_above_index], # 1
            pbest_fitnesses[neighbour_left_index], # 2
            pbest_fitnesses[neighbour_right_index], # 3
            pbest_fitnesses[neighbour_below_index], # 4
        ])

        # Update lbests:
        lbest_index = None
        if best == 0:
            lbest_index = i
        elif best == 1:
            lbest_index = neighbour_above_index
        elif best == 2:
            lbest_index = neighbour_left_index
        elif best == 3:
            lbest_index = neighbour_right_index
        else:
            lbest_index = neighbour_below_index

        lbest_indices[i] = lbest_index
        lbest_positions[i] = pbest_positions[lbest_index]
        lbest_fitnesses[i] = pbest_fitnesses[lbest_index]

    global gbest_fitness
    gbest_fitness = min(lbest_fitnesses)

def _index_above(i):
    # Given an index (in the swarm), this finds the item above that index (in the grid) and returns its index (in the swarm).
    # Get the item's position in the grid:
    i_pos = _pos_of(i, _grid)
    if i_pos is None:
        raise Exception("von_neumann_pso._index_above: did not find index {} in index map {}".format(i, _grid))
    i_row = i_pos[0]
    i_col = i_pos[1]

    # The item above the given item is at (row-1, col), possibly wrapping around.
    a_row = (i_row - 1) % _grid_rows
    # If the wrapped-around cell is empty, just go up again.
    if _grid[a_row][i_col] == -1:
        a_row = (a_row - 1) % _grid_rows

    # If we wrapped around back to the given item, warn the user.
    if _grid[a_row][i_col] == i:
        warnings.warn("von_neumann_pso._index_above: item {} is its own neighbour! Your swarm may be too small.".format(i))

    return _grid[a_row][i_col].astype(int)

def _index_below(i):
    # Given an index (in the swarm), this finds the item below that index (in the grid) and returns its index (in the swarm).
    # Get the item's position in the grid:
    i_pos = _pos_of(i, _grid)
    if i_pos is None:
        raise Exception("von_neumann_pso._index_below: did not find index {} in index map {}".format(i, _grid))

    i_row = i_pos[0]
    i_col = i_pos[1]

    # The item below the given item is at (row+1, col), possibly wrapping around.
    a_row = (i_row + 1) % _grid_rows
    # If the wrapped-around cell is empty, just go down again.
    if _grid[a_row][i_col] == -1:
        a_row = (a_row + 1) % _grid_rows

    # If we wrapped around back to the given item, warn the user.
    if _grid[a_row][i_col] == i:
        warnings.warn("von_neumann_pso._index_below: item {} is its own neighbour! Your swarm may be too small.".format(i))

    return _grid[a_row][i_col].astype(int)

def _index_left_of(i):
    # Given an index (in the swarm), this finds the item to the left of that index (in the grid) and returns its index (in the swarm).
    # Get the item's position in the grid:
    i_pos = _pos_of(i, _grid)
    if i_pos is None:
        raise Exception("von_neumann_pso._index_left_of: did not find index {} in index map {}".format(i, _grid))

    i_row = i_pos[0]
    i_col = i_pos[1]

    # The item to the left of the given item is at (row, col-1), possibly wrapping around.
    a_col = (i_col - 1) % _grid_cols
    # If the wrapped-around cell is empty, just go left again.
    if _grid[i_row][a_col] == -1:
        a_col = (a_col - 1) % _grid_cols

    # If we wrapped around back to the given item, warn the user.
    if _grid[i_row][a_col] == i:
        warnings.warn("von_neumann_pso._index_left_of: item {} is its own neighbour! Your swarm may be too small.".format(i))

    return _grid[i_row][a_col].astype(int)

def _index_right_of(i):
    # Given an index (in the swarm), this finds the item to the right of that index (in the grid) and returns its index (in the swarm).
    # Get the item's position in the grid:
    i_pos = _pos_of(i, _grid)
    if i_pos is None:
        raise Exception("von_neumann_pso._index_right_of: did not find index {} in index map {}".format(i, _grid))

    i_row = i_pos[0]
    i_col = i_pos[1]

    # The item to the right of the given item is at (row, col+1), possibly wrapping around.
    a_col = (i_col + 1) % _grid_cols
    # If the wrapped-around cell is empty, just go left again.
    if _grid[i_row][a_col] == -1:
        a_col = (a_col + 1) % _grid_cols

    # If we wrapped around back to the given item, warn the user.
    if _grid[i_row][a_col] == i:
        warnings.warn("von_neumann_pso._index_right_of: item {} is its own neighbour! Your swarm may be too small.".format(i))

    return _grid[i_row][a_col].astype(int)

def _side_of_smallest_square_containing(n):
    # Returns the side length (in items) of the smallest square that can contain n items.
    # E.g. 3 items can fit in a 2x2 square, so the result will be 2.
    # E.g. 5 items can fit in a 3x3 square, so the result will be 3.
    _sqrt = np.sqrt(float(n))
    _ceil = np.ceil(_sqrt)
    return int(_ceil)

def _rows_of_square_filled(s, n):
    # In a square with side length s, returns how many rows are filled by n items.
    # E.g. 5 items fill 2 rows in a 3x3 square, so the result will be 2.
    # E.g. 7 items fill 3 rows in a 3x3 square, so the result will be 3.
    # Also sanity-checks that there's enough space in the square.
    if np.square(s) < n:
        raise Exception("in _rows_of_square_filled: {} items don't fit in a {} by {} square.".format(n, s, s))
    _quot = float(n) / float(s)
    _ceil = np.ceil(_quot)
    return int(_ceil)

def _pos_of(val, matrix):
    # Returns the (row, col) coordinates of val in matrix,
    # or None if matrix doesn't contain val.
    for (r, row) in enumerate(matrix):
        for (c, cell) in enumerate(row):
            if cell == val:
                return (r, c)
    return None

def _position_is_within_bounds(position):
    # A position is considered to be within the bounds of the search space only if
    # each dimension component is within those bounds.
    for position_j in position:
        if position_j < lower_bound or position_j > upper_bound:
            return False
    return True

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

    velocity = -(positions[index]) + lbest_positions[index] + inertia_component + local_search_component

    position = lbest_positions[index] + inertia_component + local_search_component

    fitness = function(position)

    velocities[index] = velocity

    positions[index] = position

    fitnesses[index] = fitness


    if fitness < pbest_fitnesses[index] and _position_is_within_bounds(position):
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

    velocity = inertia_component + cognitive_component + social_component

    position = positions[index] + velocity

    fitness = function(position)

    velocities[index] = velocity

    positions[index] = position

    fitnesses[index] = fitness

    # If we have an improved and valid solution, update the pbest.
    if fitness < pbest_fitnesses[index] and _position_is_within_bounds(position):
        pbest_fitnesses[index] = fitness
        pbest_positions[index] = position

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

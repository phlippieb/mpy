import numpy as np
import warnings

# PSO parameters
w = None
c1 = None
c2 = None

# Swarm variables
swarm_size = 0
positions = None
velocities = None
fitnesses = None
pbest_positions = None # each particle's personal best
pbest_fitnesses = None
lbest_positions = None # each particle's local best
lbest_fitnesses = None

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

    _init_grid()
    _update_lbests()


def init_pso_defaults():
    global w
    w =  0.729844
    global c1
    c1 = 1.49618
    global c2
    c2 = 1.49618


def iterate():
    # Performs one iteration of the algorithm.
    # Afterwards, the swarm's velocities, positions, fitnesses, personal best positions,
    # personal best fitnesses, and local best positions and fitnesses will be updated.
    # Requires the algorithm's and swarm's parameters to have been initialized.
    _validate_algorithm()
    _validate_swarm()

    global velocities
    global positions
    global fitnesses
    global pbest_positions
    global pbest_fitnesses
    global gbest_position

    inertia_component = w * velocities

    r1 = np.random.rand(swarm_size, num_dimensions)
    cognitive_component = c1 * r1 * (pbest_positions - positions)

    r2 = np.random.rand(swarm_size, num_dimensions)
    social_component = c2 * r2 * (lbest_positions - positions)

    unclamped_velocities = inertia_component + cognitive_component + social_component
    velocities = _clamped_velocities(unclamped_velocities)

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

    _update_lbests()


def _update_lbests():
    # Updates the lbest_positions and lbest_fitnesses of the swarm.
    # Each particle's neighbourhood consists of the particles adjacent to it on a 2D grid.
    # The local best particle in each neighbourhood is the particle with best fitness.
    _validate_search_space()

    global swarm_size
    global num_dimensions
    global lbest_positions
    global lbest_fitnesses
    lbest_positions = np.zeros((swarm_size, num_dimensions))
    lbest_fitnesses = np.zeros(swarm_size)

    for i in range(0, swarm_size):
        neighbour_above_index = _index_above(i)
        neighbour_left_index = _index_left_of(i)
        neighbour_right_index = _index_right_of(i)
        neighbour_below_index = _index_below(i)

        neighbour_above_position = pbest_positions[neighbour_above_index]
        neighbour_left_position = pbest_positions[neighbour_left_index]
        neighbour_right_position = pbest_positions[neighbour_right_index]
        neighbour_below_position = pbest_positions[neighbour_below_index]

        neighbour_above_fitness = function(neighbour_above_position)
        neighbour_left_fitness = function(neighbour_left_position)
        neighbour_right_fitness = function(neighbour_right_position)
        neighbour_below_fitness = function(neighbour_below_position)

        if neighbour_above_fitness < fitnesses[i]:
            lbest_positions[i] = neighbour_above_position
            lbest_fitnesses[i] = neighbour_above_fitness
        elif neighbour_left_fitness < fitnesses[i]:
            lbest_positions[i] = neighbour_left_position
            lbest_fitnesses[i] = neighbour_left_fitness
        elif neighbour_right_fitness < fitnesses[i]:
            lbest_positions[i] = neighbour_right_position
            lbest_fitnesses[i] = neighbour_right_fitness
        elif neighbour_below_fitness < fitnesses[i]:
            lbest_positions[i] = neighbour_below_position
            lbest_fitnesses[i] = neighbour_below_fitness
        else:
            lbest_positions[i] = positions[i]
            lbest_fitnesses[i] = fitnesses[i]

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
    if _grid[a_row][i_col] == -1:
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
    if _grid[a_row][i_col] == -1:
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
    if _grid[i_row][a_col] == -1:
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
    if _grid[i_row][a_col] == -1:
        warnings.warn("von_neumann_pso._index_right_of: item {} is its own neighbour! Your swarm may be too small.".format(i))

    return _grid[i_row][a_col].astype(int)

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
    _grid = np.full((_grid_rows, _grid_cols), -1)

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
        raise Exception("lbest_pso.function was not set")
    if num_dimensions is None:
        raise Exception("lbest_pso.num_dimensions was not set")
    if lower_bound is None:
        raise Exception("lbest_pso.lower_bound was not set")
    if upper_bound is None:
        raise Exception("lbest_pso.upper_bound was not set")
    _did_validate_search_space = True


_did_validate_algorithm = False
def _validate_algorithm():
    global _did_validate_algorithm
    if _did_validate_algorithm:
        return
    if w is None:
        raise Exception("lbest_pso.w was not set")
    if c1 is None:
        raise Exception("lbest_pso.c1 was not set")
    if c2 is None:
        raise Exception("lbest_pso.c2 was not set")
    _did_validate_algorithm = True


_did_validate_swarm = False
def _validate_swarm():
    global _did_validate_swarm
    if _did_validate_swarm:
        return
    if positions is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if velocities is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if fitnesses is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if pbest_positions is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if pbest_fitnesses is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if lbest_positions is None:
        raise Exception("lbest_pso.init_swarm was not called")
    if lbest_fitnesses is None:
        raise Exception("lbest_pso.init_swarm was not called")
    _did_validate_swarm = True

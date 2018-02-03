import numpy as np

def progressive_random_walk(domain_min, domain_max, n, num_steps, max_step_size):
    # A 2D array where each row represents a step in the walk, and each column represents a dimension of the position of such a step.
    walk = np.full((num_steps, n), 0, dtype=float)
    
    # The "starting zone" of the random walk is a zone along half of the edges of all dimensions, centered around one of the corners.
    # The corner is represented by a "binary string" of sorts. -1 indicates the side of the domain min, and +1 indicates the side of the domain max.
    # Select a random starting zone:
    starting_zone = np.random.choice([-1, 1], size=([n]))
    
    # Select a random initial position from the starting zone:
    for i in range(0, n):
        # For this dimension, select a random point within half the domain of the dimension:
        r = np.random.uniform(0, (domain_max - domain_min) / 2)
        
        if starting_zone[i] == -1:
            # If the starting zone string contains a zero for this dimension, set the position to r away from the domain min:
            walk[0][i] = domain_min + r
        else:
            # Else, set the position to r away from the domain max:
            walk[0][i] = domain_max - r
    
    # Select a single random dimension and move the starting position to the edge in that dimension:
    i = np.random.choice(range(0, n))
    if starting_zone[i] == 0:
        walk[0][i] = domain_min
    else:
        walk[0][i] = domain_max
    
    # Perform num_steps random steps:
    for s in range(1, num_steps):
        # Create a position at each dimension:
        for i in range(0, n):
            # Select a random step size up to max_step_size in the direction away from the starting_zone for this dimension:
            r = np.random.uniform(0, max_step_size) * starting_zone[i] * -1
            
            # Step by the selected step size:
            walk[s][i] = walk[s-1][i] + r
            
            # If the step goes outside the function's bounds, move it back inside, and flip the starting zone's bit for this dimension
            if walk[s][i] < domain_min:
                d = domain_min - walk[s][i]
                walk[s][i] = walk[s][i] + d
                starting_zone[i] *= -1
                
            elif walk[s][i] > domain_max:
                d = walk[s][i] - domain_max
                walk[s][i] = walk[s][i] - d
                starting_zone[i] *= -1
                    
    return walk
    
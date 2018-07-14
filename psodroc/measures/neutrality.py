import progressive_random_walk as walk

# This file contains functions that estimate the neutrality of a fitness landscape.
# It contains two such functions: PN, which indicates the proportion of neutral areas encountered during a random walk,
# and LSN, which indicates the longest sub-sequence of neutral areas encountered during a random walk.
# The result of PN is a scalar value in [0, 1], with higher values indicating more overall neutrality in the landscape.
# The result of LSN is a scalar value in [0, 1], with higher values indicating that neutral areas in the landscape are more connected.


def PN_LSN(function, domain_min, domain_max, dimensions, epsilon=1e-8, step_size_fraction=.02):
    starting_zones = walk.get_starting_zones(dimensions)
    # Limit the starting zones
    starting_zones = starting_zones[:100]

    num_steps = walk.get_num_steps(dimensions, step_size_fraction)
    step_size = walk.get_step_size(domain_min, domain_max, step_size_fraction)

    num_neutral_structures = 0
    max_lsn = 0.
    num_total_structures = 0

    for (i, starting_zone) in enumerate(starting_zones):
        print '[neutrality] walk', i, '/', len(starting_zones), ': walking...'
        xs = walk.walk(dimensions, domain_min, domain_max,
                       num_steps, step_size, starting_zone)

        fitnesses = [function(x) for x in xs]

        S = _string(fitnesses, epsilon)

        num_neutral_structures += S.count(0)
        num_total_structures += len(S)
        longest_neutral_subsequence_length = 0
        current_neutral_subsequence_length = 0
        for s in S:
            if s == 0:
                # This is a neutral structure. Increment and record the current subsequence length.
                current_neutral_subsequence_length += 1
                longest_neutral_subsequence_length = max(
                    longest_neutral_subsequence_length, current_neutral_subsequence_length)
            else:
                # This is a non-neutral structure. Reset the current subsequence length.
                current_neutral_subsequence_length = 0

        # Determine the proportion of neutral structures in the longest subsequence for this walk.
        lsn = float(longest_neutral_subsequence_length) / float(len(S))

        # Record the maximum proportion.
        max_lsn = max(max_lsn, lsn)

    pn = float(num_neutral_structures) / float(num_total_structures)
    lsn = max_lsn
    return pn, lsn


def _PN(walks, function, epsilon):
    num_neutral_structures = 0
    num_total_structures = 0

    for xs in walks:
        # Handle each walk individually.
        fitnesses = [function(x) for x in xs]
        S = _string(fitnesses, epsilon)

        # Update the number of  neutral structures (indicated by 0s).
        num_neutral_structures += S.count(0)

        # Update the total number of structures.
        num_total_structures += len(S)

    # Return the proportion of neutral structures.
    return float(num_neutral_structures) / float(num_total_structures)


def _LSN(walks, function, epsilon):
    max_lsn = 0.

    for xs in walks:
        # Keep track of the longest neutral subsequence encountered during this walk.
        longest_neutral_subsequence_length = 0

        # Get a list of symbols.
        fitnesses = [function(x) for x in xs]
        S = _string(fitnesses, epsilon)

        # Iterate through the symbols to determine the length of the longest subsequence.
        current_neutral_subsequence_length = 0
        for s in S:
            if s == 0:
                # This is a neutral structure. Increment and record the current subsequence length.
                current_neutral_subsequence_length += 1
                longest_neutral_subsequence_length = max(
                    longest_neutral_subsequence_length, current_neutral_subsequence_length)
            else:
                # This is a non-neutral structure. Reset the current subsequence length.
                current_neutral_subsequence_length = 0

        # Determine the proportion of neutral structures in the longest subsequence for this walk.
        num_total_structures = len(S)
        lsn = float(longest_neutral_subsequence_length) / \
            float(num_total_structures)

        # Record the maximum proportion.
        max_lsn = max(max_lsn, lsn)

    # Return the maximum proportion of neutral structures from all walks.
    return max_lsn


def _string(fitnesses, E):
    # Build a string of symbols indicating whether groups of 3 adjacent fitnesses form neutral or non-neutral structures.
    # A structure is neutral if the largest difference between its components are less than the given allowable error.
    # Neutral structures are indicated by 0s, and non-neutral structures by 1s.
    string = []
    fitness_groups = [(fitnesses[i], fitnesses[i+1], fitnesses[i+2])
                      for i in range(0, len(fitnesses) - 2)]

    for group in fitness_groups:
        if max(group) - min(group) < E:
            string.append(0)
        else:
            string.append(1)

    return string

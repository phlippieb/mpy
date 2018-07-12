from __future__ import division  # make division cast to double by default
from decimal import *
import math
import progressive_random_walk as random_walk
import util.find as find
import itertools
import numpy as np
from util import norm

# This file contains functions that estimate the ruggedness of a fitness landscape using first entropic measures.
# It contains two such functions: FEM_0.1, which is used to measure the macro-ruggedness of the landscape, and FEM_0.01, which measures the micro-ruggedness.
# The result is a scalar value in [0, 1]. A result of 0 indicates a totally smooth landscape, and 1 indicates maximal ruggedness.

# A FEM function works as follows:
# 1. Sample fitness values from the landscape from a progressive walk. The step size of the walk is fixed for each measure. For FEM_0.1, it is the size of the domain * 0.1, and for FEM_0.01 it is the size of the domain * 0.01.
# 2. Create entropy strings from the sample and calculate the entropy of the strings for multiple sensitivity values (E). Start with E=0, and increment E by 0.05 until the entropy string contains all 0s (and the entropy is 0).
# 3. Return the max entropy found in 2.

# Given a fitness function, this function returns a value in [0, 1] indicating the macro ruggedness of the given function. A result of 0 indicates that the given function is completely flat. A result of 1 indicates that the given function is maximally rugged.


def FEM_0_1(function, domain_min, domain_max, dimensions, verbose=False):
    return _FEM(function, domain_min, domain_max, dimensions, 0.1, verbose=verbose)


def FEM_0_01(function, domain_min, domain_max, dimensions, verbose=False):
    return _FEM(function, domain_min, domain_max, dimensions, 0.01, verbose=verbose)


def _FEM(function, domain_min, domain_max, dimensions, max_step_size_fraction, verbose):
    starting_zones = random_walk.get_starting_zones(dimensions)
    # Take up to n starting zones
    starting_zones = starting_zones[:100]

    # Approach 1:
    # num_steps = walk.get_num_steps(dimensions, max_step_size_fraction)
    # step_size = walk.get_step_size(
    #     domain_min, domain_max, max_step_size_fraction)

    # Approach 2 (Malan's thesis):
    num_steps = 1000
    step_size = random_walk.get_step_size(
        domain_min, domain_max, max_step_size_fraction)

    max_entropy = 0

    # Handle each walk individually.
    for (i, starting_zone) in enumerate(starting_zones):
        if verbose:
            print '[FEM] Walk', i+1, '/', len(starting_zones)
        walk = random_walk.walk(dimensions, domain_min,
                                domain_max, num_steps, step_size, starting_zone)

        if verbose:
            print '[FEM] Getting fitnesses'
        fs = [function(xs) for xs in walk]

        if verbose:
            print '[FEM] normalising fitnesses between', min(
                fs), 'and', max(fs)
        fs = norm.norm(fs, min(fs), max(fs), Decimal(0.), Decimal(1.))

        # Find the stability measure (E_star).
        if verbose:
            print '[FEM] Getting stability'
        E_star = find_stability2(fs)

        if verbose:
            print '[FEM] Getting max entropy'
        for E in np.arange(0, E_star, .05 * E_star):
            string = _string(fs, E)

            # Update the max entropy so far.
            entropy = _entropy(string)
            max_entropy = max(entropy, max_entropy)

            E += (.05 * E_star)

    return max_entropy


def find_stability2(fs):
    return find.smallest_2(lambda E: _is_stable(fs, E), max_decimal_points=3)
    # return find.smallest(lambda E: _is_stable(fs, E), min_e=-3)


def _is_stable(fs, E):
    for i in range(len(fs)-1):
        if abs(fs[i] - fs[i+1]) > E:
            return False
    return True


def _string(fs, E):
    string = [_symbol(f1, f2, E) for f1, f2 in zip(fs[:-1], fs[1:])]
    # is_flat = np.count_nonzero(string) == 0
    return string  # , is_flat


def _symbol(f1, f2, E):
    if abs(f1 - f2) <= E:
        return 0
    elif f1 - f2 < -E:
        return -1
    else:
        return 1


_pq_permutations = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]


def _entropy(entropy_string):
    # Compute the probability of the substring [p, q] in entropy_string for each p and q in [-1, 0, 1] such that p != q.
    # (This gives the probability of each non-flat symbol.)
    # permutations = itertools.permutations([-1, 0, 1], 2)
    global _pq_permutations
    Ps = [_probability(p, q, entropy_string) for p, q in _pq_permutations]
    # Return the entropy based on those probabilities:
    return -sum(0 if P == 0 else (P * math.log(P, 6)) for P in Ps)


def _probability(p, q, entropy_string):
    # Returns the number of occurrences of pq in the given string, divided by the length of the string.

    # Count the number of times p and q occur consecutively in the string:
    occurrences = sum(1 if p_ == p and q_ == q else 0 for p_,
                      q_ in zip(entropy_string[:-1], entropy_string[1:]))

    # The probability of pq is the number of occurrences out of the length of the string.
    return occurrences / len(entropy_string)

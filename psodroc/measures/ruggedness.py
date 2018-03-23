from __future__ import division # make division cast to double by default
import math
import progressive_random_walk as walk
import itertools

# This file contains functions that estimate the ruggedness of a fitness landscape using first entropic measures.
# It contains two such functions: FEM_0.1, which is used to measure the macro-ruggedness of the landscape, and FEM_0.01, which measures the micro-ruggedness.
# The result is a scalar value in [0, 1]. A result of 0 indicates a totally smooth landscape, and 1 indicates maximal ruggedness.

# A FEM function works as follows:
# 1. Sample fitness values from the landscape from a progressive walk. The step size of the walk is fixed for each measure. For FEM_0.1, it is the size of the domain * 0.1, and for FEM_0.01 it is the size of the domain * 0.01.
# 2. Create entropy strings from the sample and calculate the entropy of the strings for multiple sensitivity values (E). Start with E=0, and increment E by 0.05 until the entropy string contains all 0s (and the entropy is 0).
# 3. Return the max entropy found in 2.

# Given a fitness function, this function returns a value in [0, 1] indicating the macro ruggedness of the given function. A result of 0 indicates that the given function is completely flat. A result of 1 indicates that the given function is maximally rugged.


def FEM_0_1(function, domain_min, domain_max, dimensions):
    return _FEM(function, domain_min, domain_max, dimensions, 0.1)

def FEM_0_01(function, domain_min, domain_max, dimensions):
    return _FEM(function, domain_min, domain_max, dimensions, 0.01)

def _FEM(function , domain_min, domain_max, dimensions, max_step_size_fraction):
    # Get fitnesses from a progressive random walk:
    max_step_size = (domain_max - domain_min) * max_step_size_fraction
    xs = walk.progressive_random_walk(domain_min, domain_max, dimensions, 1000, max_step_size)
    walk_fitnesses = [function(x) for x in xs]
    
    # Set the entropy estimation sensitivity to 0 to begin with:
    E = 0
    entropies = []
    
    # Increment E by 0.05 until the resulting entropy string is flat.
    # Calculate the entropy of the string for each E.
    while True:
        entropy_string = _entropy_string(walk_fitnesses, E)
        if _is_entropy_string_flat(entropy_string):
            break
        entropy = _entropy(entropy_string)
        entropies.append(entropy)
        E += .05
    
    # The entropy metric is the max entropy for all values of E tried.
    return max(entropies)
    
# Build a string of symbols indicating pair-wise changes in the given array of fitnesses.
# A difference between a pair of fitnesses that is less than the sensitivity parameter E is represented by a 0.
# A difference larger than E is represented by -1 or +1, depending on which fitness in the pair is larger.
def _entropy_string(fitnesses, E):
    string = []
    fitness_pairs = [(fitnesses[i], fitnesses[i+1]) for i in range(0, len(fitnesses) - 1)]
    for f0, f1 in fitness_pairs:
        if abs(f0 - f1) <= E:   string.append(0)
        elif f0 - f1 < -E:      string.append(-1)
        elif f0 - f1 > E:       string.append(1)
    return string
            
def _entropy(entropy_string):
    # Compute the probability of the substring [p, q] in entropy_string for each p and q in [-1, 0, 1] such that p != q.
    # (This gives the probability of each non-flat symbol.)
    Ps = [_probability(p, q, entropy_string) for p, q in itertools.permutations([-1, 0, 1], 2)]
    # Return the entropy based on those probabilities:
    # TODO: the 0 if P == 0 part is needed because log breaks otherwise, but it is not specified in the log formula. Check it out.
    return -sum(0 if P == 0 else (P * math.log(P, 6)) for P in Ps)
    

# Returns the number of occurences of pq in the given string, divided by the length of the string.
def _probability(p, q, entropy_string):
    # Count the number of times p and q occur consecutively in the string:
    occurences = sum(1 if p_ == p and q_ == q else 0 for p_, q_ in zip(entropy_string[:-1], entropy_string[1:]))
    # The probability of pq is the number of occurences out of the length of the string.
    return occurences / len(entropy_string)
    
# True if and only if the string contains only 0s, indicating no significant differences in fitnesses in the walk.
def _is_entropy_string_flat(entropy_string):
    if 1 in entropy_string or -1 in entropy_string:
        return False
    else:
        return True
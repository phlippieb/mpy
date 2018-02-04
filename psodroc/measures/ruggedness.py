import math
import progressive_random_walk as walk

# This file contains functions that estimate the ruggedness of a fitness landscape using first entropic measures.
# It contains two such functions: FEM_0.1, which is used to measure the macro-ruggedness of the landscape, and FEM_0.01, which measures the micro-ruggedness.
# The result is a scalar value in [0, 1]. A result of 0 indicates a totally smooth landscape, and 1 indicates maximal ruggedness.

# A FEM function works as follows:
# 1. Sample fitness values from the landscape from a progressive walk. The step size of the walk is fixed for each measure. For FEM_0.1, it is the size of the domain * 0.1, and for FEM_0.01 it is the size of the domain * 0.01.
# 2. Create entropy strings from the sample and calculate the entropy of the strings for multiple sensitivity values (E). Start with E=0, and increment E by 0.05 until the entropy string contains all 0s (and the entropy is 0).
# 3. Return the max entropy found in 2.

# Given a fitness function, this function returns a value in [0, 1] indicating the macro ruggedness of the given function. A result of 0 indicates that the given function is completely flat. A result of 1 indicates that the given function is maximally rugged.


def FEM_0_1(function, dimensions):
    return _FEM(function, dimensions, 0.1)

def FEM_0_01(function, dimensions):
    return _FEM(function, dimensions, 0.01)

def _FEM(function, dimensions, max_step_size_fraction):
    # Get fitnesses from a progressive random walk:
    domain_min = function.min(0)
    domain_max = function.max(0)
    max_step_size = (domain_max - domain_min) * max_step_size_fraction
    walk_positions = walk.progressive_random_walk(domain_min, domain_max, dimensions, 1000, max_step_size)
    walk_fitnesses = function.function(walk_positions)
    
    # Set the entropy estimation sensitivity to 0 to begin with:
    E = 0
    entropies = []
    
    while True:
        entropy_string = _entropy_string(walk_fitnesses, E)
        if _is_entropy_string_flat(entropy_string):
            break
        entropy = _entropy(entropy_string)
        entropies.append(entropy)
        E += .05
    
    return max(entropies)
    
def _entropy_string(fitnesses, E):
    # TODO: check that len(fitnesses) > 1
    string = []
    fitness_pairs = [(fitnesses[i], fitnesses[i+1]) for i in range(0, len(fitnesses) - 1)]
    for pair in fitness_pairs:
        if abs(pair[0] - pair[1]) <= E:
            string.append(0)
        
        elif pair[0] - pair[1] < -E:
            string.append(-1)
            
        elif pair[0] - pair[1] > E:
            string.append(1)
    
    return string
            
            
    
def _entropy(entropy_string):
    sum = 0
    for p in [-1, 0, 1]:
        for q in [-1, 0, 1]:
            if p != q:
                P = _probability(p, q, entropy_string)
                if P != 0:
                    sum += (P * math.log(P, 6))
    return -sum

def _probability(p, q, entropy_string):
    occurences = 0
    for i in range(0, len(entropy_string) - 1):
        if entropy_string[i] == p and entropy_string[i+1] == q:
            occurences += 1
    return occurences / len(entropy_string)
    
def _is_entropy_string_flat(entropy_string):
    if 1 in entropy_string or -1 in entropy_string:
        return False
    else:
        return True
    # return entropy_string.contains(1) or entropy_string.contains(-1)
    # for symbol in entropy_string:
    #     if symbol != 0:
    #         return False
    # return True    

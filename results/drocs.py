# This file provides results for diversity-rate-of-change experiments.
# Calling `get` will cause a lookup for the result in the local DB.
# If the result already exists, it will be returned.
# If not, it will be calculated and stored for future queries.
# 30 diversity measurements are used to determine a single diversity rate-of-change result.
# The diversity measurements are obtained using the `diversities` module of this (the `results`) package.

import diversities
import psodroc.measures.two_piecewise_linear_approximation as tpwla

def get(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations):
    existing_result = _fetch(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations)
    if existing_result is None:
        new_result = _calculate(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations)
        _store(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations, new_result)
        return new_result
    else:
        return existing_result
    
def _fetch(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations):
    # TODO: 
    # fetch from DB if available
    return None
    
def _store(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations, result):
    # TODO:
    # store to db
    pass

def _calculate(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations):
    xs, ys = diversities.get(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations)
    droc = tpwla.fit_to(xs, ys).m1
    return droc

# This file provides results for diversity experiments.
# Calling `get` will cause a lookup for the result in the local DB.
# If the result already exists, it will be returned.
# If not, it will be calculated and stored for future queries.

import psos, benchmarks
import psodroc.measures.diversity as diversity

def get(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations):
    # If the requested result exists, return it
    existing_result = _fetch_existing(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations)
    if existing_result is None:
        result = _calculate(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations)
        _store(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations, result)
        return result
    else:
        return existing_result

def _fetch_existing(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations):
    # TODO:
    # Fetch this result from the db if it exists; else return None
    return None
    
def _store(experiment_num, pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations, result):
    # TODO: store this result into the db
    pass

def _calculate(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, num_iterations):
    print " - calculating..."
    # Set up the PSO for a single diversity experiment
    pso = psos.get(pso_name)
    benchmark = benchmarks.get(benchmark_name)
    pso.function = benchmark.function
    pso.lower_bound = benchmark.min(0)
    pso.upper_bound = benchmark.max(0)
    pso.num_dimensions = benchmark_dimensions
    pso.init_pso_defaults()
    pso.init_swarm(size=pso_population_size)
    
    # Initialize the x and y values for diversity measurements taken
    diversity_xs = []
    diversity_ys = []
    
    # For each iteration of the PSO algorithm, take a diversity measurement.
    for i in range(0, num_iterations):
        print "\r -", (i*100)/num_iterations, "percent complete...                         ",
        xs = pso.positions
        diversity_measurement = diversity.avg_distance_around_swarm_centre(xs)
        diversity_xs.append(i)
        diversity_ys.append(diversity_measurement)
        pso.iterate()
    print "\r - done.                                      "
    
    # Return the diversity measurements
    return diversity_xs, diversity_ys

# This file provides results for diversity experiments.
# Calling `get` will cause a lookup for the result in the local DB.
# If the result already exists, it will be returned.
# If not, it will be calculated and stored for future queries.

import psos, benchmarks
import psodroc.measures.diversity as diversity
import db.diversities as db_diversities

# Assume we will never need more than 20k iterations per experiment
_max_iterations = 20000

def get(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment):
    # If the requested result exists, return it
    existing_result = _fetch_existing(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment)
    if existing_result is None:
        new_results = _calculate(pso_name, pso_population_size, benchmark_name, benchmark_dimensions)
        for (iteration, new_result) in enumerate(new_results):
            _store(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, new_result)
        return new_results[iteration]
    else:
        print(' - result exists; returning now.')
        return existing_result

def _fetch_existing(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment):
    return db_diversities.fetch(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment)
    
def _store(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, result):
    db_diversities.store(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, result)

def _calculate(pso_name, pso_population_size, benchmark_name, benchmark_dimensions):
    print " - result not found. calculating..."
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
    diversity_ys = []
    
    # For each iteration of the PSO algorithm, take a diversity measurement.
    for i in range(0, _max_iterations):
        print "\r -", (i*100)/_max_iterations, "percent complete...                         ",
        xs = pso.positions
        diversity_measurement = diversity.avg_distance_around_swarm_centre(xs)
        diversity_ys.append(diversity_measurement)
        pso.iterate()
    print "\r - done.                                      "
    
    # Return the diversity measurements
    return diversity_ys

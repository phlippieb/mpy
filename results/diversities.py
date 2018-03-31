# This file provides results for diversity experiments.
# Calling `get` will cause a lookup for the result in the local DB.
# If the result already exists, it will be returned.
# If not, it will be calculated and stored for future queries.

import psos, benchmarks
import psodroc.measures.diversity as diversity
import db.diversity_table as diversity_table
import print_time as t

# Assume we will never need more than 10k iterations per experiment
_max_iterations = 10000

def get(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, force_calculation=False, verbose=False):
    # If the requested result exists, return it
    existing_result = None
    if not force_calculation:
        existing_result = _fetch_existing(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment)

    if force_calculation or existing_result is None:
        print t.now(), "     - diversity result not found. calculating for", _max_iterations, "iterations..."
        new_results = _calculate(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, verbose=verbose)

        print t.now(), '     - storing', len(new_results), 'diversity results...'
        for (iteration, new_result) in enumerate(new_results):
            _store(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, new_result)
        diversity_table.commit()

        print t.now(), '     - done.'
        return new_results[iteration]
    else:
        return existing_result

def _fetch_existing(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment):
    return diversity_table.fetch(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment)

def _store(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, result):
    diversity_table.store(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, iteration, experiment, result)

def _calculate(pso_name, pso_population_size, benchmark_name, benchmark_dimensions, verbose=False):
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
    if verbose:
        prev_perc = -1
        perc_increment = 1

    for i in range(0, _max_iterations):
        if verbose:
            perc = (i*100)/_max_iterations
            if perc > prev_perc + (perc_increment - 1):
                prev_perc = perc
                print t.now(), '     -', perc, 'percent complete...'

        xs = pso.positions
        diversity_measurement = diversity.avg_distance_around_swarm_centre(xs)
        diversity_ys.append(diversity_measurement)
        pso.iterate()

    if verbose:
        print t.now(), '     - 100 percent complete.'

    # Return the diversity measurements
    return diversity_ys

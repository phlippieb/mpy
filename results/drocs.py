# This file provides results for diversity-rate-of-change experiments.
# Calling `get` will cause a lookup for the result in the local DB.
# If the result already exists, it will be returned.
# If not, it will be calculated and stored for future queries.
# The diversity measurements are obtained using the `diversities` module of this (the `results`) package.

import diversities
import psodroc.measures.two_piecewise_linear_approximation as tpwla
import db.droc_table as droc_table
import print_time as t


def get(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, force_calculation=False, verbose=False):
    # Status report
    if verbose:
        print t.now(), '   - getting droc',
        print ':', pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num

    existing_result = None
    if not force_calculation:
        existing_result = _fetch(
            pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num)
    elif verbose:
        print t.now(), '   - forcing calculation.'

    if force_calculation or existing_result is None:
        if verbose:
            print t.now(), '   - droc result not found. calculating...'
        new_result = _calculate(pso_name, swarm_size, benchmark_name, dimensionality,
                                num_iterations, experiment_num, force_calculation=force_calculation, verbose=verbose)
        if verbose:
            print t.now(), '   - storing droc result...'
        _store(pso_name, swarm_size, benchmark_name, dimensionality,
               num_iterations, experiment_num, new_result)
        if verbose:
            print t.now(), '   - done.'
        return new_result
    else:
        return existing_result


def _fetch(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num):
    return droc_table.fetch(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num)


def _store(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, result):
    droc_table.store(pso_name, swarm_size, benchmark_name,
                     dimensionality, num_iterations, experiment_num, result)
    droc_table.commit()


def _calculate(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, force_calculation=False, verbose=False):
    xs = range(0, num_iterations)
    ys = [diversities.get(pso_name, swarm_size, benchmark_name, dimensionality, x, experiment_num,
                          verbose=verbose, force_calculation=(force_calculation and x == 0)) for x in xs]
    droc = tpwla.fit_to(xs, ys).m1
    return droc

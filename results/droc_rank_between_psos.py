import drocs
from rank import rank
from db import droc_rank_between_psos_table
import print_time as t

def get(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, verbose=False, benchmark=False):
    print t.now(), ' - getting rank between psos',
    print ':', pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations

    if benchmark:
        # Don't try and fetch existing result, and don't store result
        _calculate(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, verbose=verbose)
    else:
        existing_result = _fetch(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations)
        if existing_result is None:
            print t.now(), '   - droc rank between pso\'s not found. calculating...'
            new_result = _calculate(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, verbose=verbose)
            print t.now(), '   - storing result...'
            _store(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, new_result)
            return new_result
        else:
            return existing_result

def _fetch(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations):
    return droc_rank_between_psos_table.fetch(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations)

def _store(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, rank):
    # Store result for pso_1_name, pso_2_name (as given):
    droc_rank_between_psos_table.store(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, rank)
    # Store inverted result for inverted order (pso_2_name, pso_1_name):
    droc_rank_between_psos_table.store(pso_2_name, pso_1_name, swarm_size, benchmark_name, dimensionality, num_iterations, rank * -1)
    droc_rank_between_psos_table.commit()

def _calculate(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, verbose=False):
    experiment_nums = range(0, 30)
    pso_1_drocs = [drocs.get(pso_1_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, verbose=verbose) for experiment_num in experiment_nums]
    pso_2_drocs = [drocs.get(pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, verbose=verbose) for experiment_num in experiment_nums]
    result = rank.rank(pso_1_drocs, pso_2_drocs)
    return result

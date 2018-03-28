import drocs
from rank import rank
from db import droc_rank_between_psos_table

def get(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, progress=None, progress_total=None):
    # Status report
    print ' - getting rank between psos',
    if progress is not None and progress_total is not None:
        print progress, 'of', progress_total,
    print ':', pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations
    
    # Actions
    existing_result = _fetch(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations)
    if existing_result is None:
        print '   - droc rank between pso\'s not found. calculating...'
        new_result = _calculate(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations)
        print '   - storing result...'
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
    
def _calculate(pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations):
    experiment_nums = range(0, 30)
    pso_1_drocs = [drocs.get(pso_1_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num) for experiment_num in experiment_nums]
    pso_2_drocs = [drocs.get(pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num) for experiment_num in experiment_nums]
    result = rank.rank(pso_1_drocs, pso_2_drocs)
    return result

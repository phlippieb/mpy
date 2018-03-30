import results.droc_rank_between_psos as rank
import results.drocs as drocs
import benchmarks

_configs = []
_prep_configs = []
    
def process(batch_num, num_batches, prep=False):
    all_pso_names = [
        # 'alternative_barebones_pso', 
        # 'barebones_pso', 
        'gbest_pso', 
        'gc_gbest_pso', 
        'gc_lbest_pso', 
        'gc_von_neumann_pso', 
        'lbest_pso', 
        'social_only_pso', 
        'von_neumann_pso'
    ]
        
    all_swarm_sizes = [
        5, 
        10, 
        25, 
        50, 
        75, 
        100,
        500
    ]
    
    all_benchmark_names = [
        'spherical', # Unimodal, smooth, simple
        'rastrigin', # Rugged, unimodal on macro-scale
        'rosenbrock', # Smooth, multimodal in 4 dimensions and up
        'weierstrass' # Rugged on micro- and macro-scale
    ]
    
    all_dimensionalities = [
        5,
        25,
        50,
        100,
        500,
        1000
    ]
    
    all_nums_iterations = [
        25, 
        50, 
        75, 
        100,
        125, 
        150, 
        2000, 
        10000
    ]
    
    global _configs
    
    # Configurations for comparing DRoC performance for different swarm sizes:
    # (with fixed 5D benchmarks and 2000 iterations per PSO)
    if prep:
        _make_prep_configs(all_pso_names, all_swarm_sizes, all_benchmark_names, [5], [2000])
    else:
        _make_configs(all_pso_names, all_swarm_sizes, all_benchmark_names, [5], [2000])
    
    # Configurations for comparing DRoC performance at different dimensions:
    # (with fixed 25-particle swarms and 2000 iterations)
    if prep:
        _make_prep_configs(all_pso_names, [25], all_benchmark_names, all_dimensionalities, [2000])
    else:
        _make_configs(all_pso_names, [25], all_benchmark_names, all_dimensionalities, [2000])
    
    # Configurations for comparing DRoC performance at different numbers of iterations:
    # (with fixed 25-particle swarms and 5D benchmarks)
    if prep:
        _make_prep_configs(all_pso_names, [25], all_benchmark_names, [5], all_nums_iterations)
    else:
        _make_configs(all_pso_names, [25], all_benchmark_names, [5], all_nums_iterations)
    
    # Process all the configs (in batches as specified):
    if prep:
        num_configs = len(_prep_configs)
        batch_indices = range(batch_num, num_configs, num_batches)
        batch_size = len(batch_indices)
        
        for (i, index) in enumerate(batch_indices):
            prep_config = _prep_configs[index]
            print 'DRoC', i, 'of', batch_size
            drocs.get(*prep_config)
        
    else:
        num_configs = len(_configs)
        batch_indices = range(batch_num, num_configs, num_batches)
        batch_size = len(batch_indices)
    
        for (i, index) in enumerate(batch_indices):
            config = _configs[index]
            print 'Rank', i, 'of', batch_size
            rank.get(*config)
        

def _make_configs(pso_names, swarm_sizes, benchmark_names, dimensionalities, nums_iterations):
    print 'determining configurations...'
    print '(processing', len(pso_names), 'pso names,', len(swarm_sizes), 'swarm sizes,', len(benchmark_names), 'benchmark names,', len(dimensionalities), 'dimensionalities, and', len(nums_iterations), 'numbers of iterations)'
    
    global _configs
    
    for pso_1_i in range(0, len(pso_names)-1):
        pso_1_name = pso_names[pso_1_i]
        for pso_2_i in range(pso_1_i+1, len(pso_names)):
            pso_2_name = pso_names[pso_2_i]
            if pso_1_name == pso_2_name:
                continue
            for swarm_size in swarm_sizes:
                for benchmark_name in benchmark_names:
                    benchmark = benchmarks.get(benchmark_name)
                    for dimensionality in dimensionalities:
                        if not benchmark.is_dimensionality_valid(dimensionality):
                            continue
                        for num_iterations in nums_iterations:
                            config = (pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations)
                            _configs.append(config)
    print 'done.'
    
def _make_prep_configs(pso_names, swarm_sizes, benchmark_names, dimensionalities, nums_iterations):
    global _prep_configs
    
    for pso_name in pso_names:
        for swarm_size in swarm_sizes:
            for benchmark_name in benchmark_names:
                for dimensionality in dimensionalities:
                    benchmark = benchmarks.get(benchmark_name)
                    for dimensionality in dimensionalities:
                        if not benchmark.is_dimensionality_valid(dimensionality):
                            continue
                        for num_iterations in nums_iterations:
                            for experiment_num in range(0, 30):
                                prep_config = (pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num)
                                _prep_configs.append(prep_config)

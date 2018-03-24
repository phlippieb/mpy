import drocs
import benchmarks

pso_names = ['alternative_barebones_pso', 'barebones_pso', 'gbest_pso', 'gc_gbest_pso', 'gc_lbest_pso', 'gc_von_neumann_pso', 'lbest_pso', 'social_only_pso', 'von_neumann_pso']
swarm_sizes = [2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
benchmark_names = ['ackley', 'alpine', 'beale', 'bohachevsky1_generalized', 'eggholder', 'goldstein_price', 'griewank', 'levy13_generalized', 'michalewicz', 'pathological', 'quadric', 'quartic', 'rastrigin', 'rosenbrock', 'salomon', 'schwefel_2_22', 'schwefel_2_26', 'six_hump_camel_back', 'skew_rastrigin', 'spherical', 'step', 'weierstrass', 'zakharov']
dimensionalities = [1, 2, 3, 4, 5, 10, 20, 30]
num_iterations = [10, 20, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
experiment_nums = range(0, 30)

def _num_valid_configurations():
    num_valid_benchmark_dimensionality_configs = 0
    # Determine the number of valid benchmark/dimensionality combinations:
    for benchmark_name in benchmark_names:
        for dimensionality in dimensionalities:
            benchmark = benchmarks.get(benchmark_name)
            if benchmark.is_dimensionality_valid(dimensionality):
                num_valid_benchmark_dimensionality_configs += 1
    # Determine the total number of valid configurations:
    return len(pso_names) * len(swarm_sizes) * num_valid_benchmark_dimensionality_configs * len(num_iterations) * len(experiment_nums)

def _get_configuration(index):
    i = 0
    for pso_name in pso_names:
        for swarm_size in swarm_sizes:
            for benchmark_name in benchmark_names:
                for dimensionality in dimensionalities:
                    for iterations in num_iterations:
                        for experiment_num in experiment_nums:
                            benchmark = benchmarks.get(benchmark_name)
                            if benchmark.is_dimensionality_valid(dimensionality):
                                if i == index:
                                    configuration = (pso_name, swarm_size, benchmark_name, dimensionality, iterations, experiment_num)
                                    return configuration
                                else:
                                    i += 1
                                    

# def _process(configurations):
#     for (i, configuration) in enumerate(configurations):
#         print "getting droc result", i, "of", len(configurations),
#         print configuration
#         drocs.get(*configuration)
        
def process(block_num, num_blocks):
    print 'total configurations:', _num_valid_configurations()
    block_indices = range(block_num, _num_valid_configurations(), num_blocks)
    # configurations = [_get_configuration(i) for i in block_indices]
    # print 'block_size:', len(configurations)
    # _process(configurations)
    _process_indices(block_indices)
    
def _process_indices(indices):
    for i in indices:
        configuration = _get_configuration(i)
        print "getting droc result", i, "of", len(indices), ':', configuration
        drocs.get(*configuration)

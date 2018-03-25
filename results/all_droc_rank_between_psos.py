import results.droc_rank_between_psos as rank
import benchmarks

pso_names = [
    'alternative_barebones_pso', 
    'barebones_pso', 
    'gbest_pso', 
    # 'gc_gbest_pso', 
    # 'gc_lbest_pso', 
    # 'gc_von_neumann_pso', 
    'lbest_pso', 
    'social_only_pso', 
    'von_neumann_pso']

swarm_sizes = [
    2,
    3, 
    5,  
    25, 
    2000,
    5000]
    
benchmark_names = [
    # 'ackley', 
    'alpine', 
    # 'beale', 
    # 'bohachevsky1_generalized', 
    # 'eggholder', 
    # 'goldstein_price', 
    'griewank', 
    # 'levy13_generalized', 
    # 'michalewicz', 
    # 'pathological', 
    # 'quadric', 
    # 'quartic', 
    # 'rastrigin', 
    # 'rosenbrock', 
    # 'salomon', 
    # 'schwefel_2_22', 
    'schwefel_2_26', 
    # 'six_hump_camel_back', 
    # 'skew_rastrigin', 
    # 'spherical', 
    # 'step', 
    'weierstrass']
    # 'zakharov']
    
dimensionalities = [
    5,
    25,
    50,
    100]
    
nums_iterations = [
    25, 
    50, 
    75, 
    100,
    125, 
    150, 
    2000, 
    10000]
    
def process(batch_num, num_batches):
    _make_configs()
    num_configs = len(_configs)
    batch_indices = range(batch_num, num_configs, num_batches)
    batch_size = len(batch_indices)
    
    for (i, index) in enumerate(batch_indices):
        config = _configs[index]
        print ' -', i, 'of', batch_size
        rank.get(*config)
        
_configs = []

def _make_configs():
    if len(_configs) > 0:
        return
    
    print 'determining configurations',
    for i in range(0, len(pso_names)):
        for j in range(i+1, len(pso_names)):
            print '.',
            # All combinations are allowed except for ABBPSO and anything besides BBPSO (for now)
            pso_1_name = pso_names[i]
            pso_2_name = pso_names[j]
            if pso_1_name != 'alternative_barebones_pso' or pso_2_name == 'barebones_pso':
                for swarm_size in swarm_sizes:
                    for benchmark_name in benchmark_names:
                        for dimensionality in dimensionalities:
                            if benchmarks.get(benchmark_name).is_dimensionality_valid(dimensionality):
                                for num_iterations in nums_iterations:
                                    config = (pso_1_name, pso_2_name, swarm_size, benchmark_name, dimensionality, num_iterations)
                                    _configs.append(config)        
    print '\ndone.'

import drocs
import benchmarks
import psos
from time import time

pso_names = psos.all_names
swarm_sizes = [25]
benchmark_names = benchmarks.all_names
dimensionalities = [1]
num_iterations = [2000]
experiment_nums = range(30)


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
                                    configuration = (
                                        pso_name, swarm_size, benchmark_name, dimensionality, iterations, experiment_num)
                                    return configuration
                                else:
                                    i += 1


def process(block_num, num_blocks):
    print 'total configurations:', _num_valid_configurations()
    block_indices = range(block_num, _num_valid_configurations(), num_blocks)
    # configurations = [_get_configuration(i) for i in block_indices]
    # print 'block_size:', len(configurations)
    # _process(configurations)
    _process_indices(block_indices)


def benchmark():
    start_time = time()
    _benchmark(start_time)
    end_time = time()
    print "\nBenchmark time (seconds): {}\n".format(end_time - start_time)


def _process_indices(indices):
    for (index_number, i) in enumerate(indices):
        configuration = _get_configuration(i)
        print "getting droc result", index_number, "of", len(
            indices), ':', configuration
        drocs.get(*configuration)


def _benchmark(start_time):
    # 1 experiment each of Von Neumann PSO with 10, 50 and 100 particles, on the Griewank function in 5, 15 and 30 dimensions, up to 10k iterations.
    # (So 3 x 3 = 9 experiments.)
    i = 0
    for swarm_size in [10, 50, 100]:
        for dimensionality in [5, 15, 30]:
            for num_iterations in [10000]:
                print 'experiment', i, "of", 9
                print 'time after start:', time() - start_time
                drocs.get('von_neumann_pso', swarm_size, 'griewank',
                          dimensionality, num_iterations, 1, force_calculation=True)
                i += 1

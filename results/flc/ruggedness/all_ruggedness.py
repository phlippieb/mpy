from results.flc.ruggedness import fem_0_1, fem_0_01
from results import benchmarks


def process(batch_num, num_batches, verbose):
    config = _config(batch_num)
    while config is not None:
        benchmark_name, dimensionality, experiment = config
        benchmark = benchmarks.get(benchmark_name)
        if benchmark.is_dimensionality_valid(dimensionality):
            print 'FEM_0.1:  getting', benchmark_name, dimensionality, experiment
            fem_0_1.get(benchmark_name, dimensionality,
                        experiment, verbose=verbose)
            print 'FEM_0.01: getting', benchmark_name, dimensionality, experiment
            fem_0_01.get(benchmark_name, dimensionality,
                         experiment, verbose=verbose)

        else:
            print 'FEM: skipping', benchmark_name, dimensionality, experiment, '(invalid number of dimensions)'
        batch_num += num_batches
        config = _config(batch_num)


def _config(index):
    """Return the i'th configuration"""
    benchmark_names = benchmarks.all_names
    dimensionalities = [1, 2, 5, 25, 50, 100, 500, 1000]
    experiments = range(30)
    i = 0
    for dimensionality in dimensionalities:
        for benchmark_name in benchmark_names:
            for experiment in experiments:
                if i == index:
                    return benchmark_name, dimensionality, experiment
                else:
                    i += 1
    return None

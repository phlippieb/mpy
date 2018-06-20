from results.flc.searchability import fci_sigma
from results import benchmarks


def process(batch_num, num_batches, verbose):
    config = _config(batch_num)
    while config is not None:
        benchmark_name, dimensionality = config
        benchmark = benchmarks.get(benchmark_name)
        if benchmark.is_dimensionality_valid(dimensionality):
            print 'FCI: getting', benchmark_name, dimensionality
            fci_sigma.get(benchmark_name, dimensionality, verbose=verbose)
        else:
            print 'FCI: skipping', benchmark_name, dimensionality, '(invalid number of dimensions)'
        batch_num += num_batches
        config = _config(batch_num)


def _config(index):
    """Return the i'th configuration"""
    benchmark_names = benchmarks.all_names
    dimensionalities = [1, 2, 5, 25, 50, 100, 500, 1000]
    i = 0
    for benchmark_name in benchmark_names:
        for dimensionality in dimensionalities:
            if i == index:
                return benchmark_name, dimensionality
            else:
                i += 1
    return None

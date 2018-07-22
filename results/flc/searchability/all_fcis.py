from results.flc.searchability import fci_sigma
from results.flc.searchability import fci_cog, fci_soc
from results import benchmarks


def process(batch_num, num_batches, verbose):
    config = _config(batch_num)
    while config is not None:
        benchmark_name, dimensionality, experiment, is_soc = config
        benchmark = benchmarks.get(benchmark_name)
        if benchmark.is_dimensionality_valid(dimensionality):
            if is_soc:
                print 'FCI_soc: getting', benchmark_name, dimensionality, experiment
                # fci_sigma.get(benchmark_name, dimensionality, verbose=verbose)
                fci_soc.get(benchmark_name, dimensionality,
                            experiment, verbose=verbose)
            else:
                print 'FCI_cog: getting', benchmark_name, dimensionality, experiment
                fci_cog.get(benchmark_name, dimensionality,
                            experiment, verbose=verbose)
        else:
            print 'FCI: skipping', benchmark_name, dimensionality, '(invalid number of dimensions)'
        batch_num += num_batches
        config = _config(batch_num)


def _config(index):
    """Return the i'th configuration"""
    benchmark_names = benchmarks.all_names
    dimensionalities = [1, 2, 5, 25, 50, 100, 500]  # , 1000]
    benchmark_names = ['schwefel_2_22']
    dimensionalities = [500, 1000]
    i = 0
    for benchmark_name in benchmark_names:
        for dimensionality in dimensionalities:
            for e in range(30):
                for is_soc in [True, False]:
                    if i == index:
                        return benchmark_name, dimensionality, e, is_soc
                    else:
                        i += 1
    return None

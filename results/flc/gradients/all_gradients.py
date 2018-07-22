from results.flc.gradients import g_avg, g_dev
from results import benchmarks


def process(batch_num, num_batches, verbose):
    config = _config(batch_num)
    while config is not None:
        benchmark_name, dimensionality, experiment = config
        benchmark = benchmarks.get(benchmark_name)
        if benchmark.is_dimensionality_valid(dimensionality):
            print 'G_avg: getting', benchmark_name, dimensionality, experiment
            g_avg.get(benchmark_name, dimensionality,
                      experiment, verbose=verbose)
            print 'G_dev: getting', benchmark_name, dimensionality, experiment
            g_dev.get(benchmark_name, dimensionality,
                      experiment, verbose=verbose)
        else:
            print 'G_avg/G_dev: skipping', benchmark_name, dimensionality, experiment, '(invalid number of dimensions)'
        batch_num += num_batches
        config = _config(batch_num)


def _config(index):
    """Return the i'th configuration"""
    benchmark_names = benchmarks.all_names
    dimensionalities = [1, 2, 5, 25, 50, 100, 500]  # , 1000]
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

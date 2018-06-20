from db.flc.gradients import gradients_table
from results import benchmarks
from psodroc.measures import gradients


def get(benchmark_name, dimensionality, experiment, step_size_fraction=.02, verbose=False):
    """Fetch or calculate the gradient measures."""
    existing_results = _fetch_existing(
        benchmark_name, dimensionality, step_size_fraction, experiment)
    if existing_results is None:
        if verbose:
            print 'Measurements not found. Calculating...'
        g_avg, g_dev = _calculate(
            benchmark_name, dimensionality, step_size_fraction)
        if verbose:
            print 'Calculated. Storing...'
        _store(benchmark_name, dimensionality,
               step_size_fraction, experiment, g_avg, g_dev)
        if verbose:
            print 'Stored.'
        return g_avg, g_dev
    else:
        if verbose:
            print 'Measurements found.'
        return existing_results


def _fetch_existing(benchmark_name, dimensionality, step_size_fraction, experiment):
    """Fetch the requested measurements (g_avg and g_dev) from the database if they exists. Return None otherwise."""
    return gradients_table.fetch(benchmark_name, dimensionality, step_size_fraction, experiment)


def _store(benchmark_name, dimensionality, step_size_fraction, experiment, g_avg, g_dev):
    """Store a measurement to the database.

    Also commits the result immediately.
    """
    gradients_table.store(benchmark_name, dimensionality,
                          step_size_fraction, experiment, g_avg, g_dev)
    gradients_table.commit()


def _calculate(benchmark_name, dimensionality, step_size_fraction):
    """Calculate the requested measurement."""
    benchmark = benchmarks.get(benchmark_name)
    f = benchmark.function
    f_min = benchmark.min(0)
    f_max = benchmark.max(0)
    g_avg, g_dev = gradients.G_measures(
        f, f_min, f_max, dimensionality, step_size_fraction=step_size_fraction)
    return g_avg, g_dev

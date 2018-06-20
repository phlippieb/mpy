from db.flc.neutrality import lsn_table
from results import benchmarks
from psodroc.measures import neutrality


def get(benchmark_name, dimensionality, experiment, epsilon=1e-8, step_size_fraction=.02, verbose=False):
    """Fetch or calculate the PN measure (proportion of neutral structures in a walk)."""
    existing_result = _fetch_existing(
        benchmark_name, dimensionality, epsilon, step_size_fraction, experiment)
    if existing_result is None:
        if verbose:
            print 'Measurement not found. Calculating...'
        # Result not found. Calculate and store it.
        new_result = _calculate(
            benchmark_name, dimensionality, epsilon, step_size_fraction)
        if verbose:
            print 'Calculated. Storing...'
        _store(benchmark_name, dimensionality, epsilon,
               step_size_fraction, experiment, new_result)
        if verbose:
            print 'Stored.'
        return new_result
    else:
        if verbose:
            print 'Measurement found.'
        return existing_result


def _fetch_existing(benchmark_name, dimensionality, epsilon, step_size_fraction, experiment):
    """Fetch the requested measurement from the database if it exists. Return None if it doesn't."""
    return lsn_table.fetch(benchmark_name, dimensionality, epsilon, step_size_fraction, experiment)


def _store(benchmark_name, dimensionality, epsilon, step_size_fraction, experiment, measurement):
    """Store a measurement to the database.

    Also commits the result immediately.
    """
    lsn_table.store(benchmark_name, dimensionality, epsilon,
                    step_size_fraction, experiment, measurement)
    lsn_table.commit()


def _calculate(benchmark_name, dimensionality, epsilon, step_size_fraction):
    """Calculate the requested measurement."""
    benchmark = benchmarks.get(benchmark_name)
    f = benchmark.function
    f_min = benchmark.min(0)
    f_max = benchmark.max(0)
    _, lsn = neutrality.PN_LSN(f, f_min, f_max, dimensionality,
                               epsilon=epsilon, step_size_fraction=step_size_fraction)
    # TODO: use pn
    return lsn

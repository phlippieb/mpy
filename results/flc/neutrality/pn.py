from db.flc.neutrality import pn_table
from results import benchmarks
from psodroc.measures import neutrality


def get(benchmark_name, dimensionality, experiment, epsilon=1e-8, verbose=False):
    """Fetch or calculate the PN measure (proportion of neutral structures in a walk)."""
    existing_result = _fetch_existing(
        benchmark_name, dimensionality, epsilon, experiment)
    if existing_result is None:
        if verbose:
            print 'Measurement not found. Calculating...'
        # Result not found. Calculate and store it.
        new_result = _calculate(benchmark_name, dimensionality, epsilon)
        if verbose:
            print 'Calculated. Storing...'
        _store(benchmark_name, dimensionality, epsilon, experiment, new_result)
        if verbose:
            print 'Stored.'
        return new_result
    else:
        if verbose:
            print 'Measurement found.'
        return existing_result


def _fetch_existing(benchmark_name, dimensionality, epsilon, experiment):
    """Fetch the requested measurement from the database if it exists. Return None if it doesn't."""
    return pn_table.fetch(benchmark_name, dimensionality, epsilon, experiment)


def _store(benchmark_name, dimensionality, epsilon, experiment, measurement):
    """Store a measurement to the database.

    Also commits the result immediately.
    """
    pn_table.store(benchmark_name, dimensionality,
                   epsilon, experiment, measurement)
    pn_table.commit()


def _calculate(benchmark_name, dimensionality, epsilon):
    """Calculate the requested measurement."""
    benchmark = benchmarks.get(benchmark_name)
    f = benchmark.function
    f_min = benchmark.min(0)
    f_max = benchmark.max(0)
    pn, _ = neutrality.PN_LSN(f, f_min, f_max, dimensionality)
    # TODO: send epsilon through
    # TODO: use lsn
    return pn

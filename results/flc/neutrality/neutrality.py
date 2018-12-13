from db.flc.neutrality import neutrality_table
from results import benchmarks
from psodroc.measures import neutrality


def get(benchmark_name, dimensionality, experiment, epsilon=1e-8, step_size_fraction=.02, verbose=False, force=False):
    """Fetch or calculate the neutrality measures."""
    existing_results = None
    if not force:
        existing_results = _fetch_existing(
            benchmark_name, dimensionality, epsilon, step_size_fraction, experiment)
    if force or existing_results is None:
        if verbose:
            if force:
                print 'Calculating...'
            else:
                print 'Measurements not found. Calculating...'
        
        pn, lsn = _calculate(
            benchmark_name, dimensionality, epsilon, step_size_fraction)
        if verbose:
            print 'Calculated. Storing...'
        _store(benchmark_name, dimensionality, epsilon,
               step_size_fraction, experiment, pn, lsn)
        if verbose:
            print 'Stored.'
        return pn, lsn
    else:
        if verbose:
            print 'Measurements found.'
        pn, lsn = existing_results
        return pn, lsn


def _fetch_existing(benchmark_name, dimensionality, epsilon, step_size_fraction, experiment):
    """Fetch the requested measurement from the database if it exists. Return None if it doesn't."""
    return neutrality_table.fetch(
        benchmark_name, dimensionality, epsilon, step_size_fraction, experiment)


def _store(benchmark_name, dimensionality, epsilon, step_size_fraction, experiment, pn, lsn):
    """Store a measurement to the database.

    Also commits the result immediately.
    """
    neutrality_table.store(benchmark_name, dimensionality,
                           epsilon, step_size_fraction, experiment, pn, lsn)
    neutrality_table.commit()


def _calculate(benchmark_name, dimensionality, epsilon, step_size_fraction):
    """Calculate the requested measurement."""
    benchmark = benchmarks.get(benchmark_name)
    f = benchmark.function
    f_min = benchmark.min(0)
    f_max = benchmark.max(0)
    pn, lsn = neutrality.PN_LSN(f, f_min, f_max, dimensionality,
                                epsilon=epsilon, step_size_fraction=step_size_fraction)
    return pn, lsn

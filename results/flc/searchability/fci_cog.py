from db.flc.searchability import fci_cog_table
from results import benchmarks
from psodroc.measures import searchability


def get(benchmark_name, dimensionality, experiment, verbose=False):
    """Fetch or calculate the FCI_cog (fitness cloud index obtained with a cognitive PSO) for the given subject.

    If the measurement is available in the database, it is returned directly.
    Otherwise, it is calculated, stored for future queries, and returned.
    Parameters:
    - benchmark_name: String. The name of the benchmark function to take the measurement on.
    - dimensionality: Int. The number of dimensions to consider the benchmark function in.
    - experiment: Int. Specify which of multiple measurements to request.
    Returns:
    - measurement: Float-like. The FCI_cog measurement.
    """
    existing_result = _fetch_existing(
        benchmark_name, dimensionality, experiment)
    if existing_result is None:
        if verbose:
            print 'Measurement not found. Calculating...'
        # Result not found. Calculate and store it.
        new_result = _calculate(benchmark_name, dimensionality)
        if verbose:
            print 'Calculated. Storing...'
        _store(benchmark_name, dimensionality, experiment, new_result)
        if verbose:
            print 'Stored.'
        return new_result
    else:
        if verbose:
            print 'Measurement found.'
        return existing_result


def _fetch_existing(benchmark_name, dimensionality, experiment):
    """Fetch the requested measurement from the database if it exists. Return None if it doesn't."""
    return fci_cog_table.fetch(benchmark_name, dimensionality, experiment)


def _store(benchmark_name, dimensionality, experiment, measurement):
    """Store a measurement to the database.

    Also commits the result immediately.
    """
    fci_cog_table.store(benchmark_name, dimensionality,
                        experiment, measurement)
    fci_cog_table.commit()


def _calculate(benchmark_name, dimensionality):
    """Calculate the requested measurement."""
    benchmark = benchmarks.get(benchmark_name)
    f = benchmark.function
    f_min = benchmark.min(0)
    f_max = benchmark.max(0)
    return searchability.FCI_cog(f, f_min, f_max, dimensionality)

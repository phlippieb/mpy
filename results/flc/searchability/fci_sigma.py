from db.flc.searchability import fci_sigma_table
from results.flc.searchability import fci_cog, fci_soc
from psodroc.measures import searchability


def get(benchmark_name, dimensionality, verbose=False):
    """Fetch or calculate the FCI_sigma (mean standard deviation of multiple FCI_soc and _cog measurements).

    If the measurement is available in the database, it is returned directly.
    Otherwise, it is calculated, stored for future queries, and returned.
    Parameters:
    - benchmark_name: String. The name of the benchmark function to take the measurement on.
    - dimensionality: Int. The number of dimensions to consider the benchmark function in.
    Returns:
    - measurement: Float-like. The FCI_sigma measurement.
    """
    existing_result = _fetch_existing(
        benchmark_name, dimensionality)
    if existing_result is None:
        if verbose:
            print 'Measurement not found. Calculating...'
        new_result = _calculate(
            benchmark_name, dimensionality, verbose=verbose)
        if verbose:
            print 'Calculated. Storing...'
        _store(benchmark_name, dimensionality, new_result)
        if verbose:
            print 'Stored.'
        return new_result
    else:
        if verbose:
            print 'Measurement found.'
        return existing_result


def _fetch_existing(benchmark_name, dimensionality):
    """Fetch the requested measurement from the database if it exists. Return None if it doesn't."""
    return fci_sigma_table.fetch(benchmark_name, dimensionality)


def _store(benchmark_name, dimensionality, measurement):
    """Store a measurement to the database.

    Also commits the result immediately.
    """
    fci_sigma_table.store(benchmark_name, dimensionality, measurement)
    fci_sigma_table.commit()

# def _calculate(pso_name, swarm_size, benchmark_name, dimensionality, num_iterations, experiment_num, force_calculation=False, verbose=False):
#     xs = range(0, num_iterations)
#     ys = [diversities.get(pso_name, swarm_size, benchmark_name, dimensionality, x, experiment_num, verbose=verbose, force_calculation=(force_calculation and x == 0)) for x in xs]
#     droc = tpwla.fit_to(xs, ys).m1
#     return droc


def _calculate(benchmark_name, dimensionality, verbose):
    fci_cogs = [fci_cog.get(benchmark_name, dimensionality,
                            experiment, verbose=verbose) for experiment in range(30)]
    fci_socs = [fci_soc.get(benchmark_name, dimensionality,
                            experiment, verbose=verbose) for experiment in range(30)]
    fci_sigma = searchability.FCI_sigma(fci_socs, fci_cogs)
    return fci_sigma

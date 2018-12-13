from results.flc.neutrality import neutrality


def get(benchmark_name, dimensionality, experiment, epsilon=1e-8, step_size_fraction=.02, verbose=False, force=False):
    """Fetch or calculate the LSN measure (proportion of neutral structures in a walk)."""
    _, lsn = neutrality.get(
        benchmark_name,
        dimensionality,
        experiment,
        epsilon=epsilon,
        step_size_fraction=step_size_fraction,
        verbose=verbose,
        force=force)
    return lsn

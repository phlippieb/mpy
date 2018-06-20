from results.flc.gradients import gradients


def get(benchmark_name, dimensionality, experiment, step_size_fraction=.02, verbose=False):
    g_avg, _ = gradients.get(benchmark_name, dimensionality, experiment,
                             step_size_fraction=step_size_fraction, verbose=verbose)
    return g_avg

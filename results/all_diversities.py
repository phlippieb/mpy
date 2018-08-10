from termcolor import colored

import diversities
import benchmarks
import psos


class DiversityConfiguration:
    pso_name = ""
    swarm_size = 0
    benchmark_name = ""
    dimensionality = 0
    experiment = 0

    def __init__(self, pso_name, swarm_size, benchmark_name, dimensionality, experiment):
        self.pso_name = pso_name
        self.swarm_size = swarm_size
        self.benchmark_name = benchmark_name
        self.dimensionality = dimensionality
        self.experiment = experiment


# Which PSOs to use
pso_names = psos.all_names

# With which swarm sizes to use the PSOs
# swarm_sizes = [25]
swarm_sizes = [5, 10, 25, 50, 75, 100, 500]

# Which benchmark functions to use
# benchmark_names = ['ackley', 'alpine', 'bohachevsky1_generalized',
#    'griewank', 'levy13_generalized', 'michalewicz']
benchmark_names = ['spherical', 'rastrigin', 'rosenbrock', 'weierstrass']

# Which dimensionalities to use the benchmark functions with.
# dimensionalities = range(1, 10)
# dimensionalities = [5, 25, 50, 100, 500, 1000]
dimensionalities = [5]

# The number of independent experiments per config
experiments = range(0, 30)

configurations = []
for pso_name in pso_names:
    for swarm_size in swarm_sizes:
        for benchmark_name in benchmark_names:
            for dimensionality in dimensionalities:
                for experiment in experiments:
                    benchmark = benchmarks.get(benchmark_name)
                    if benchmark.is_dimensionality_valid(dimensionality):
                        configuration = DiversityConfiguration(
                            pso_name, swarm_size, benchmark_name, dimensionality, experiment)
                        configurations.append(configuration)


def _process_configurations(configurations, verbose=False):
    for (i, configuration) in enumerate(configurations):
        print "result", colored('{}'.format(
            i), 'cyan', attrs=['bold']), "of", colored('{}'.format(len(configurations)), 'cyan'),
        print '(', configuration.pso_name, configuration.swarm_size, configuration.benchmark_name, configuration.dimensionality, configuration.experiment, ")"
        diversities.get(
            configuration.pso_name,
            configuration.swarm_size,
            configuration.benchmark_name,
            configuration.dimensionality,
            0,
            configuration.experiment,
            verbose=verbose)


def process(group_num, num_groups, verbose=False):
    group_size = len(configurations) / num_groups
    group_start = group_size * group_num
    group_end = group_start + group_size
    group_indices = range(group_start, group_end)
    group = []
    for i in group_indices:
        if i > 0 and i < len(configurations):
            configuration = configurations[i]
            group.append(configuration)
    _process_configurations(group, verbose=verbose)

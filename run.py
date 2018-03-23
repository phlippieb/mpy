import results.diversities as diversities
import results.drocs as drocs
import results.benchmarks as benchmarks

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

pso_names = ['gc_gbest_pso', 'barebones_pso', 'social_only_pso']
swarm_sizes = [1, 2, 5, 10, 20, 50, 100]
benchmark_names = ['ackley', 'alpine', 'bohachevsky1_generalized', 'griewank', 'levy13_generalized', 'michalewicz']
dimensionalities = range(1, 10)
experiments = range(0, 30)
experiments = [0]
    
configurations = []
for pso_name in pso_names:
    for swarm_size in swarm_sizes:
        for benchmark_name in benchmark_names:
            for dimensionality in dimensionalities:
                for experiment in experiments:
                    benchmark = benchmarks.get(benchmark_name)
                    if benchmark.is_dimensionality_valid(dimensionality):
                        configuration = DiversityConfiguration(pso_name, swarm_size, benchmark_name, dimensionality, experiment)
                        configurations.append(configuration)
                    
for (i, configuration) in enumerate(configurations):
    print "result", i, "of", len(configurations),
    print "( pso =", configuration.pso_name, "swarm =", configuration.swarm_size, "benchmark =", configuration.benchmark_name, "dimensionality =", configuration.dimensionality, "experiment =", configuration.experiment, ")"
    _ = diversities.get(configuration.pso_name, configuration.swarm_size, configuration.benchmark_name, configuration.dimensionality, 0, configuration.experiment)
    
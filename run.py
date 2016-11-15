import numpy as np
import matplotlib.pyplot as plt
import os
import psodroc.benchmarks.spherical as spherical
import psodroc.pso.gbest_pso as gbest

# set up gbest to solve the spherical benchmark function

gbest.function = spherical.spherical
gbest.lower_bound = spherical.lower_bound
gbest.upper_bound = spherical.upper_bound
gbest.num_dimensions = 5
gbest.init_pso_defaults()
gbest.init_swarm(size=25)
iterations = 100

# example 1: plotting all fitnesses over time

all_fits = np.zeros([iterations, gbest.swarm_size])
for i in range(0, iterations):
    gbest.iterate()
    for index, fitness in np.ndenumerate(gbest.fitnesses):
        all_fits[i, index] = fitness
plt.plot(all_fits)
plt.show()

# example 2: writing best solutions to file
gbest.init_swarm(size=25)
solutions = []
for sample in range(0, 30):
    for iteration in range(0, iterations):
        gbest.iterate()
    solution = min(gbest.fitnesses)
    solutions.append(solution)

path = './results/fit/gbest.{}.spherical.{}'.format(gbest.swarm_size, gbest.num_dimensions)
dir = os.path.dirname(path)
if not os.path.exists(dir):
    os.makedirs(dir)
with open(path, 'w') as f:
    for solution in solutions:
        str_fitness = '{}\n'.format(solution)
        f.write(str_fitness)
f.closed

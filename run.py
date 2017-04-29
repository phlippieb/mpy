import numpy as np
import matplotlib.pyplot as plt
import os
import psodroc.benchmarks.ackley as ackley
import psodroc.pso.von_neumann_pso as pso

pso.function = ackley.ackley
pso.lower_bound = ackley.domain[0]
pso.upper_bound = ackley.domain[1]
pso.num_dimensions = 5
pso.init_pso_defaults()
pso.init_swarm(size=25)

iterations = 1000

all_fits = np.zeros([iterations, pso.swarm_size])
best_fits = []
for i in range(0, iterations):
    pso.iterate()
    for index, fitness in np.ndenumerate(pso.fitnesses):
        all_fits[i, index] = fitness
    best_fit = min(all_fits[i])
    best_fits.append(best_fit)

plt.plot(all_fits)
plt.show()

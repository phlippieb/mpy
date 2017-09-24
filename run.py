import numpy as np
import matplotlib.pyplot as plt
import os
import psodroc.benchmarks.levy13_generalized as f
import psodroc.pso.gc_lbest_pso as pso

pso.function = f.function
pso.lower_bound = f.min(0)
pso.upper_bound = f.max(0)
pso.num_dimensions = 50
pso.init_pso_defaults()
pso.init_swarm(size=10)

iterations = 1000

all_fits = np.zeros([iterations, pso.swarm_size])
best_fits = []
for i in range(0, iterations):
    pso.iterate()
    for index, fitness in np.ndenumerate(pso.fitnesses):
        all_fits[i, index] = fitness
    best_fit = min(all_fits[i])
    best_fits.append(best_fit)

print("best: {}".format(min(best_fits)))

plt.plot(best_fits)
plt.show()

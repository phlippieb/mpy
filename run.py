import numpy as np
import matplotlib.pyplot as plt
import os
import psodroc.benchmarks.ackley as ackley
import psodroc.pso.von_neumann_pso as vn

# set up Von Neumann PSO to solve the ackley benchmark function

vn.function = ackley.ackley
vn.lower_bound = ackley.domain[0]
vn.upper_bound = ackley.domain[1]
vn.num_dimensions = 5
vn.init_pso_defaults()
vn.init_swarm(size=25)

iterations = 1000

all_fits = np.zeros([iterations, vn.swarm_size])
for i in range(0, iterations):
    vn.iterate()
    for index, fitness in np.ndenumerate(vn.fitnesses):
        all_fits[i, index] = fitness
plt.plot(all_fits)
plt.show()

best_fits = []
for fits in all_fits:
    best_fit = min(fits)
    best_fits.append(best_fit)
plt.plot(best_fits)
plt.show()

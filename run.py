import numpy as np
import matplotlib.pyplot as plt
import os
import psodroc.benchmarks.ackley as ackley
import psodroc.pso.lbest_pso as lbest

# set up lbest to solve the ackley benchmark function

lbest.function = ackley.ackley
lbest.lower_bound = ackley.domain[0]
lbest.upper_bound = ackley.domain[1]
lbest.num_dimensions = 5
lbest.init_pso_defaults()
lbest.init_swarm(size=25)

iterations = 100

all_fits = np.zeros([iterations, lbest.swarm_size])
for i in range(0, iterations):
    lbest.iterate()
    for index, fitness in np.ndenumerate(lbest.fitnesses):
        all_fits[i, index] = fitness
plt.plot(all_fits)
plt.show()

best_fits = []
for fits in all_fits:
    best_fit = min(fits)
    best_fits.append(best_fit)
plt.plot(best_fits)
plt.show()

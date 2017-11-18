import numpy as np
import matplotlib.pyplot as plt
import os
import psodroc.benchmarks.levy13_generalized as f
import psodroc.pso.alternative_barebones_pso as pso
import psodroc.measures.diversity as diversity
import psodroc.measures.two_piecewise_linear_approximation as twpla

pso.function = f.function
pso.lower_bound = f.min(0)
pso.upper_bound = f.max(0)
pso.num_dimensions = 20
pso.init_pso_defaults()
pso.init_swarm(size=50)

iterations = 500

# How often (in terms of iterations) to take diversity measurements:
div_interval = 1
# Iterations at which diversity measures are taken
div_xs = []
# Diversity measurements taken
div_ys = []

# gbest fitnesses at each iteration:
gbests = []

for i in range(0, iterations):
    pso.iterate()

    # Capture diversity
    if i % div_interval == 0:
        div = diversity.avg_distance_around_swarm_centre(pso.positions)
        div_xs.append(i)
        div_ys.append(div)

    # Capture gbest
    gbests.append(pso.gbest_fitness)

# Calculate a two-piecewise linear approximation of all diversity measurements
droc = twpla.fit_to(div_xs, div_ys)

# Plot all diversity measurements as points, and the two-piecewise linear approximation of the diversity measurements as lines
plt.plot(div_xs, div_ys, ".", color="grey")
twpla.plot(len(div_xs)-1, droc)
plt.show()

plt.plot(gbests)
plt.show()

# print(gbests)

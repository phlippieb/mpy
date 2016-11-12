import numpy as np
import matplotlib.pyplot as plt
import benchmarks.spherical as spherical
import pso.gbest_pso2 as gbest

# run gbest pso to solve the sphere benchmark function

gbest.function = spherical.spherical
gbest.lower_bound = spherical.lower_bound
gbest.upper_bound = spherical.upper_bound
gbest.num_dimensions = 2
gbest.init_pso_defaults()
gbest.init_swarm(size=25)

iterations = 75
all_fits = np.zeros([iterations, gbest.swarm_size])
for i in range(0, iterations):
    gbest.iterate()
    for index, fitness in np.ndenumerate(gbest.fitnesses):
        all_fits[i, index] = fitness
plt.plot(all_fits)
plt.show()

import numpy as np
import matplotlib.pyplot as plt
import psodroc.benchmarks.spherical as spherical
import psodroc.pso.gbest_pso as gbest

# run gbest pso to solve the sphere benchmark function

gbest.function = spherical.spherical
gbest.lower_bound = spherical.lower_bound
gbest.upper_bound = spherical.upper_bound
gbest.num_dimensions = 5
gbest.init_pso_defaults()
gbest.init_swarm(size=25)

iterations = 100
all_fits = np.zeros([iterations, gbest.swarm_size])
for i in range(0, iterations):
    print 'iteration {}...'.format(i)
    gbest.iterate()
    for index, fitness in np.ndenumerate(gbest.fitnesses):
        all_fits[i, index] = fitness
plt.plot(all_fits)
plt.show()

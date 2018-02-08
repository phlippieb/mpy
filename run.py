import matplotlib.pyplot as plt
import psodroc.benchmarks.rastrigin as f
import psodroc.pso.gc_von_neumann_pso as pso
import psodroc.measures.diversity as diversity
import psodroc.measures.two_piecewise_linear_approximation as twpla

# pso.function = f.function
# pso.lower_bound = f.min(0)
# pso.upper_bound = f.max(0)
# pso.num_dimensions = 40
# pso.init_pso_defaults()
# pso.init_swarm(size=50)
# 
# iterations = 1000
# 
# # How often (in terms of iterations) to take diversity measurements:
# div_interval = 1
# # Iterations at which diversity measures are taken
# div_xs = []
# # Diversity measurements taken
# div_ys = []
# 
# # gbest fitnesses at each iteration:
# gbests = []
# 
# for i in range(0, iterations):
#     pso.iterate()
# 
#     # Capture diversity
#     if i % div_interval == 0:
#         div = diversity.avg_distance_around_swarm_centre(pso.positions)
#         div_xs.append(i)
#         div_ys.append(div)
# 
#     # Capture gbest
#     gbests.append(pso.gbest_fitness)
# 
# # Calculate a two-piecewise linear approximation of all diversity measurements
# droc = twpla.fit_to(div_xs, div_ys)
# 
# # Plot all diversity measurements as points, and the two-piecewise linear approximation of the diversity measurements as lines
# plt.plot(div_xs, div_ys, ".", color="grey")
# twpla.plot(len(div_xs)-1, droc)
# plt.show()
# 
# plt.plot(gbests)
# plt.show()

# print(gbests)

import psodroc.measures.funnels as funnels
import numpy as np  

all_disps = []
for i in range(0, 10):
    disp = funnels.dispersion_metric(f.function, f.min(0), f.max(0), 2)
    all_disps.append(disp)
    print("disp {}: {}".format(i, disp))
mean_disp = np.average(all_disps)
print("\nmean: {}".format(mean_disp))

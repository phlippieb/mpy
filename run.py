import psodroc.pso.cognitive_only_pso as cpso

import psodroc.benchmarks.spherical as benchmark

f = benchmark.function
low = benchmark.min(0)
high = benchmark.max(0)
d = 2
swarm_size = 5

cpso.init_search_space(f, d, low, high)
cpso.init_swarm(swarm_size)
cpso.init_pso_defaults()

# This gives some very weird results :)
cpso.w = .98

max_velocity = (high - low) * .1
initial_velocities = np.random.uniform(
    low=-max_velocity, high=max_velocity, size=[swarm_size, d])
cpso.velocities = initial_velocities

import psodroc.measures.diversity as diversity
diversities = []
fitnesses = []

num_iterations = 100
iterations = range(num_iterations)
for i in iterations:
    div = diversity.avg_distance_around_swarm_centre(cpso.positions)
    diversities.append(div)
    fit = min(cpso.fitnesses)
    fitnesses.append(fit)
    cpso.iterate()

# Normalize to [0, 1]

# def normalize(x, mn, mx):
#     return (x - mn) / (mx - mn)

# div_min, div_max = (np.min(diversities), np.max(diversities))
# diversities = [normalize(div, div_min, div_max) for div in diversities]

# f_min, f_max = (np.min(fitnesses), np.max(fitnesses))
# fitnesses = [normalize(fit, f_min, f_max) for fit in fitnesses]

import matplotlib.pyplot as plt
plt.ylim(ymin=0, ymax=np.max(diversities) + .5)
plt.plot(iterations, diversities, color='green')  # , linestyle=":")
# plt.plot(iterations, fitnesses, color='blue')#, linestyle=':')
plt.show()

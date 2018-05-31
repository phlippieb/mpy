import psodroc.measures.progressive_manhattan_walk as walk
import matplotlib.pyplot as plt

for walk in walk.multiple_walks(2, -1, 1, 0.1):
    xs, ys = (walk.T[0], walk.T[1])
    plt.plot(xs, ys, linestyle='--')

plt.show()

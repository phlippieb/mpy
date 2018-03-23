import results.diversities as diversities

for i in range(0, 30):
    print "experiment", i
    xs, ys = diversities.get(i, 'gbest_pso', 100, 'ackley', 5, 100)
    print ys[0], ys[20], ys[40], ys[60], ys[80]
    
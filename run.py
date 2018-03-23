import results.diversities as diversities
import results.drocs as drocs

for i in range(0, 30):
    print "experiment", i
    droc = drocs.get(i, 'gbest_pso', 10, 'griewank', 10, 1000)
    print 'droc', i, '=', droc

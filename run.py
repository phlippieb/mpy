import psodroc.measures.ruggedness as ruggedness
import numpy as np
from termcolor import colored

import psodroc.benchmarks.griewank as benchmark
f = benchmark.function
f_min = benchmark.min(0)
f_max = benchmark.max(0)
# ds = [1, 2, 5, 15, 30]
ds = [1000]

for d in ds:
    print colored('{}D'.format(d), 'blue')
    fem1s = []
    fem01s = []
    samples = 30
    for i in range(samples):
        print colored('running {} of {} samples...'.format(
            i+1, samples), 'white'), '\r',
        fem01 = ruggedness.FEM_0_01(f, f_min, f_max, d)
        fem01s.append(fem01)
    print '                                             \r',
    print 'FEM 0.01:', np.average(fem01s)

    for i in range(samples):
        print colored('running {} of {} samples...'.format(
            i+1, samples), 'white'), '\r',
        fem1 = ruggedness.FEM_0_1(f, f_min, f_max, d)
        fem1s.append(fem1)
    print '                                             \r',
    print 'FEM 0.1: ',  np.average(fem1s)

    print ''

print colored('done.', 'green')

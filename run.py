import psodroc.measures.gradients as gradients
import numpy as np
from termcolor import colored

import psodroc.benchmarks.ackley as benchmark
f = benchmark.function
f_min = benchmark.min(0)
f_max = benchmark.max(0)
ds = [1, 2, 5, 15, 30]

for d in ds:
    print colored('{} dimensions:'.format(d), 'blue')
    g_avgs = []
    g_devs = []
    samples = 30
    for i in range(samples):
        print colored('running {} of {} samples...'.format(
            i+1, samples), 'white'), '\r',
        g_avg, g_dev = gradients.G_measures(f, f_min, f_max, d)
        g_avgs.append(g_avg)
        g_devs.append(g_dev)
    g_avg = np.average(g_avgs)
    g_dev = np.average(g_devs)
    print '                                             \r',
    print 'avg:', g_avg, '\ndev:', g_dev
    print ''
print colored('done.', 'green')

"""
Expected values (Ackley):

D   | avg | dev
--- | --- | ---
1   | 13  | 8
2   | 33  | 22
5   | 35  | 20
15  | 3.5 | 2.9
30  | 3.8 | 3.1
"""

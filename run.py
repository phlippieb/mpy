# -*- coding: utf-8 -*-

import psodroc.measures.funnels as funnels
import psodroc.benchmarks.spherical as benchmark
import numpy as np
dimensionality = 1

a = []
for i in range(30):
    b = funnels.DM(
        benchmark.function, benchmark.min(0), benchmark.max(0), dimensionality)
    a.append(b)
c = np.mean(a)
print 'Result:\t', c

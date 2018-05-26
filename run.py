# -*- coding: utf-8 -*-

import psodroc.measures.ruggedness as ruggedness
import psodroc.benchmarks.spherical as benchmark
import numpy as np
dimensionality = 1

f_01 = []
for i in range(30):
    r_01 = ruggedness.FEM_0_01(
        benchmark.function, benchmark.min(0), benchmark.max(0), dimensionality)
    f_01.append(r_01)
a_01 = np.mean(f_01)
print '0.01:\t', a_01

f_1 = []
for i in range(30):
    r_1 = ruggedness.FEM_0_1(
        benchmark.function, benchmark.min(0), benchmark.max(0), dimensionality)
    f_1.append(r_1)
a_1 = np.mean(f_1)
print '0.1:\t', a_1

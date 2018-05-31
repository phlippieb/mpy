# -*- coding: utf-8 -*-

import psodroc.measures.funnels as funnels
import psodroc.benchmarks.spherical as benchmark1
import psodroc.benchmarks.schwefel_2_26 as benchmark2
import numpy as np
import matplotlib.pyplot as plt

dimensionality = 1

dms1 = []
dms2 = []
for i in range(30):
    dms1.append(funnels.DM(benchmark1.function, benchmark1.min(0),
                           benchmark1.max(0), dimensionality))
    dms2.append(funnels.DM(benchmark2.function, benchmark2.min(0),
                           benchmark2.max(0), dimensionality))

plt.plot(dms1, np.zeros_like(dms1), 'x', color='blue')
plt.plot(dms2, np.zeros_like(dms1), 'x', color='red')
plt.show()

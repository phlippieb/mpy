import matplotlib.pyplot as plt
import psodroc.benchmarks.rastrigin as f
import psodroc.pso.gc_von_neumann_pso as pso
import psodroc.measures.ruggedness as ruggedness

r = ruggedness.FEM_0_01(f.function, f.min(0), f.max(0), 1)
print(r)
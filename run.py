from termcolor import colored
import psodroc.measures.searchability as searchability

import psodroc.benchmarks.rastrigin as benchmark
f = benchmark.function
f_min = benchmark.min(0)
f_max = benchmark.max(0)
ds = [1, 2, 5, 15, 30]
# ds = [5]

for d in ds:
    print colored('{}D'.format(d), 'blue')
    fci_soc, fci_cog, fci_sig = searchability.FCIs(f, f_min, f_max, d)
    print '{:.3f}'.format(fci_cog), '{:.3f}'.format(fci_soc)
    print ''

print colored('done.', 'green')

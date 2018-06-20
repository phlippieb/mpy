from results.flc.searchability import fci_cog, fci_soc, fci_sigma

print '\n-- This should calculate one from scratch:'
print fci_cog.get('ackley', 1, 0, verbose=True)
print '\n-- This should not:'
print fci_cog.get('ackley', 1, 0, verbose=True)
print '\n-- This should calculate all but one from scratch:'
print fci_sigma.get('ackley', 1, verbose=True)
print '\n-- This should not:'
print fci_sigma.get('ackley', 1, verbose=True)

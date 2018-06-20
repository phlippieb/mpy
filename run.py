from results.flc.deception import fdc

print '\n-- This should calculate from scratch:'
print fdc.get('step', 1, 0, verbose=True)
print '\n-- And this should not:'
print fdc.get('step', 1, 0, verbose=True)

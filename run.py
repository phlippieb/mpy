from results.flc.funnels import dm

print '\n-- This should calculate from scratch:'
print dm.get('step', 1, 0, verbose=True)
print '\n-- And this should not:'
print dm.get('step', 1, 0, verbose=True)

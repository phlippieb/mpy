from results.flc.neutrality import pn, lsn

print '\n-- This should calculate from scratch:'
print pn.get('step', 1, 0, verbose=True)
print '\n-- And this should not:'
print lsn.get('step', 1, 0, verbose=True)
print '\n-- And this should:'
print lsn.get('step', 1, 1, verbose=True)
print '\n-- And this should not:'
print pn.get('step', 1, 1, verbose=True)

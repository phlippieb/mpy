from results.flc.neutrality import pn
from results.flc.neutrality import lsn

pn0 = pn.get('step', 1, 0, verbose=True)
lsn0 = lsn.get('step', 1, 0, verbose=True)

print 'PN 0:', pn0
print 'LSN 0:', lsn0

lsn1 = lsn.get('step', 1, 1, verbose=True)
pn1 = pn.get('step', 1, 1, verbose=True)

print 'PN 1:', pn1
print 'LSN 1:', lsn1

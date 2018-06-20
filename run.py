from results.flc.gradients import g_avg, g_dev

print '\n-- This should calculate from scratch:'
print g_avg.get('ackley', 1, 0, verbose=True)
print '\n-- And this should not:'
print g_dev.get('ackley', 1, 0, verbose=True)
print '\n-- And this should:'
print g_dev.get('ackley', 1, 1, verbose=True)
print '\n-- And this should not:'
print g_avg.get('ackley', 1, 1, verbose=True)

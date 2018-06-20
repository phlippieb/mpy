from optparse import OptionParser
from results.flc.deception import all_fdcs
from results.flc.funnels import all_funnels
from results.flc.gradients import all_gradients

parser = OptionParser()
parser.add_option('--batch', dest='batch_number')
parser.add_option('--of', dest='total_batches')
parser.add_option('-v', '--verbose', dest='verbose',
                  action='store_true', default=False)
options, args = parser.parse_args()
batch_number = options.batch_number
total_batches = options.total_batches
verbose = options.verbose

if verbose:
    print 'Verbose mode is on.'

if batch_number is not None and total_batches is not None:
    print 'processing batch', batch_number, 'of', total_batches, 'batches...'
    all_fdcs.process(int(batch_number), int(total_batches), verbose=verbose)
    all_funnels.process(int(batch_number), int(total_batches), verbose=verbose)
    all_gradients.process(int(batch_number), int(
        total_batches), verbose=verbose)

elif batch_number is not None:
    raise Exception(
        'When providing a batch_number arg, a total_batches arg is required.')

elif total_batches is not None:
    raise Exception(
        'When providing a total_blocks arg, a batch_number arg is required.')

else:
    all_gradients.process(0, 1, verbose)
    all_funnels.process(0, 1, verbose)
    all_fdcs.process(0, 1, verbose)

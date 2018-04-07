from optparse import OptionParser
import results.all_droc_rank_between_psos as ranks

parser = OptionParser()
parser.add_option('--batch', dest='batch_number')
parser.add_option('--of', dest='total_batches')
parser.add_option('--benchmark', dest="is_benchmark", action="store_true", default=False)
parser.add_option('--prep', dest='prep', action='store_true', default=False)
parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False)
options, args = parser.parse_args()
is_benchmark = options.is_benchmark
batch_number = options.batch_number
total_batches = options.total_batches
prep = options.prep
verbose = options.verbose

if is_benchmark:
    print 'benchmarking'
    ranks.benchmark()

else:
   if prep:
       print 'Running in prep mode.'

   if verbose:
       print 'Verbose mode is on.'

   if batch_number is not None and total_batches is not None:
       print 'processing batch', batch_number, 'of', total_batches, 'batches...'
       ranks.process(int(batch_number), int(total_batches), prep, verbose)

   elif batch_number is not None:
       raise Exception('When providing a batch_number arg, a total_batches arg is required.')

   elif total_batches is not None:
       raise Exception('When providing a total_blocks arg, a batch_number arg is required.')

   else:
       ranks.process(0, 1, prep, verbose)

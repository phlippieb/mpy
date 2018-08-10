from optparse import OptionParser
from results.flc.deception import all_fdcs
from results.flc.funnels import all_funnels
from results.flc.gradients import all_gradients
from results.flc.neutrality import all_neutralities
from results.flc.ruggedness import all_ruggedness
from results.flc.searchability import all_fcis
from results import all_diversities, all_drocs, all_droc_rank_between_psos

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


def _run(batch_number, total_batches, verbose):
    b = int(batch_number)
    t = int(total_batches)
    # print 'processing batch', batch_number, 'of', total_batches, 'batches...'
    # all_fcis.process(b, t, verbose)
    # all_gradients.process(b, t, verbose)
    # all_funnels.process(b, t, verbose)
    # all_fdcs.process(b, t, verbose)
    # all_neutralities.process(b, t, verbose)
    # all_ruggedness.process(b, t, verbose)

    all_diversities.process(b, t, verbose=verbose)
    # all_drocs.process(b, t, verbose=verbose)
    # all_droc_rank_between_psos.process(b, t, verbose=verbose)


if batch_number is not None and total_batches is not None:
    _run(batch_number, total_batches, verbose)

elif batch_number is not None:
    raise Exception(
        'When providing a batch_number arg, a total_batches arg is required.')

elif total_batches is not None:
    raise Exception(
        'When providing a total_blocks arg, a batch_number arg is required.')

else:
    _run(0, 1, verbose)

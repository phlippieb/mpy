from optparse import OptionParser
import results.all_drocs as drocs

parser = OptionParser()
parser.add_option('--block', dest='block_number')
parser.add_option('--of', dest='total_blocks')
options, args = parser.parse_args()
block_number = int(options.block_number)
total_blocks = int(options.total_blocks)

if block_number is not None and total_blocks is not None:
    print 'processing block', block_number, 'of', total_blocks, 'droc result blocks...'
    drocs.process(block_number, total_blocks)
    
elif block_number is not None:
    raise Exception('When providing a block_number arg, a total_blocks arg is required.')
    
elif total_blocks is not None:
    raise Exception('When providing a total_blocks arg, a block_number arg is required.')

else:
    print 'processing all droc results...'
    # drocs.process(0, 1)

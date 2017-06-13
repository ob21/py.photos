from __future__ import unicode_literals
import logging
from optparse import OptionParser

logging.basicConfig(filename='photos.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filemode='w')
logging.info('Photos.py logs')

parser = OptionParser()
parser.add_option("-i", "--input", dest="input_dir",
                  help="input dir", metavar="INPUT_DIR")
parser.add_option("-o", "--output", dest="output_dir",
                  help="output dir", metavar="OUTPUT_DIR")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")
(options, args) = parser.parse_args()

print("input dir = " + str(options.account_id))
print("output dir = " + str(options.output_dir))

input_dir = "./"
output_dir = "./photos/"
if options.account_id is not None:
    user_id = str(options.account_id)
if options.output_dir is not None:
    dir = str(options.output_dir)

logging.info("input dir is " + input_dir)
logging.info("output dir is " + output_dir)


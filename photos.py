from __future__ import unicode_literals
import os
import logging
from pathlib import Path
import exifread
from datetime import datetime
from optparse import OptionParser

logging.basicConfig(filename='photos.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filemode='w')
logging.info('Photos.py logs')

parser = OptionParser()
parser.add_option("-i", "--input", dest="input_dir",
                  help="photos input directory")
parser.add_option("-o", "--output", dest="output_dir",
                  help="photos output directory")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")
(options, args) = parser.parse_args()

print("input dir = " + str(options.input_dir))
print("output dir = " + str(options.output_dir))

input_dir = "input"
output_dir = "output"
if options.input_dir is not None:
    input_dir = str(options.input_dir)
if options.output_dir is not None:
    output_dir = str(options.output_dir)

print("input dir is " + input_dir)
logging.info("input dir is " + input_dir)
print("output dir is " + output_dir)
logging.info("output dir is " + output_dir)

for p in Path(input_dir).glob('./**/*'):
    print()
    print(p)
    if p.is_file():
        ext = os.path.splitext(p)[1]
        if ext == ".JPG":
            print("is a file :" + str(p))
            with open('.\\' + str(p), 'rb') as my_picture:
                tags = exifread.process_file(my_picture)
                print('try to get exif data for ' + '.\\' + str(p))
                new_name = os.path.basename(p)
                try:
                    picture_date = datetime.strptime(str(
                        tags.get('EXIF DateTimeOriginal')),
                        '%Y:%m:%d %H:%M:%S')
                    new_name = datetime.strptime(str(
                        tags.get('EXIF DateTimeOriginal')),
                        '%Y_%m_%d_'+os.path.basename(p))
                    print(picture_date)
                except ValueError:
                    picture_date = None
                    print("No value for %s" % p)
            print(output_dir + "\\" + new_name + ext)
            # os.rename(p, os.path.dirname(p) + new_name)
        else:
            print("is not a .JPG file : " + ext)

# Get the date of the photo
# filename = '.\\input\\593APPLE\\IMG_2002.JPG'
# with open(filename, 'rb') as my_picture:
#     tags = exifread.process_file(my_picture)
#     print('try to get exif data for '+filename)
#     try:
#         picture_date = datetime.strptime(str(
#             tags.get('EXIF DateTimeOriginal')),
#             '%Y:%m:%d %H:%M:%S')
#         print(picture_date)
#     except ValueError:
#         picture_date = None
#         print("No value for %s" % filename)

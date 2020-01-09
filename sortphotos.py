from __future__ import unicode_literals
import os
from shutil import copyfile
from shutil import rmtree
import logging
from pathlib import Path
import exifread
from datetime import datetime
from datetime import date
from optparse import OptionParser

logging.basicConfig(filename='photos.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filemode='w')
logging.info('Photos.py logs')

parser = OptionParser()
parser.add_option("-i", "--input", dest="input_dir",
                  help="photos input directory")
parser.add_option("-o", "--output", dest="output_dir",
                  help="photos output directory")
parser.add_option("-p", "--prefix", dest="prefix",
                  help="photos output directory")                 
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")
(options, args) = parser.parse_args()

print("input dir = " + str(options.input_dir))
print("output dir = " + str(options.output_dir))
print("prefix = " + str(options.prefix))

input_dir = "input"
output_dir = "output"
prefix = ""
if options.input_dir is not None:
    input_dir = str(options.input_dir)
if options.output_dir is not None:
    output_dir = str(options.output_dir)
if options.prefix is not None:
    prefix = str(options.prefix)

print("input dir is " + input_dir)
logging.info("input dir is " + input_dir)
print("output dir is " + output_dir)
logging.info("output dir is " + output_dir)
print("prefix is " + prefix)
logging.info("prefix is " + prefix)

rmtree(output_dir, ignore_errors=True)

for p in Path(input_dir).glob('./**/*'):
    #print()
    print(p)
    #print(p.resolve())
    #print(os.sep)
    if p.is_file():
        ext = os.path.splitext(str(p))[1]
        img_types = [".JPG", ".JPEG", ".PNG", ".GIF"]
        vid_types = [".MOV", ".MP4", ".MPG", ".MPEG", ".AVI"]
        if ext in img_types:
            #print("is an IMAGE file : " + str(p))
            with open('.' + os.sep + str(p), 'rb') as my_picture:
                tags = exifread.process_file(my_picture)
                #print('try to get exif data for ' + '.\\' + str(p))
                #print("tags : "+str(tags))
                # print(str(tags.get('EXIF DateTimeOriginal')))
                try:
                    date = datetime.strptime(str(
                            tags.get('EXIF DateTimeOriginal')),
                            '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    date = date.today()
                #print("date = " + str(date))
                year = date.year
                #print("year = " + str(year))
                month = date.month
                #print("month = " + str(month))
            file = os.path.basename(str(p))
            #print(file)
            newfile = prefix + "_" + file
            #print("newfile = " + newfile)
            newpath = output_dir + os.sep + str(year) + os.sep + str(month) + os.sep + newfile
            print("newpath = " + newfile)
            i=0
            while os.path.exists(newpath):
                i = i + 1
                newpath = output_dir + os.sep + str(year) + os.sep + str(month) + os.sep + str(i) + "_" + newfile
            print(newpath)
            if not os.path.exists(output_dir + os.sep + str(year) + os.sep + str(month) + os.sep):
                os.makedirs(output_dir + os.sep + str(year) + os.sep + str(month) + os.sep)
            #os.rename(p, newpath)
            copyfile(str(p), newpath)
        elif ext in vid_types:
            #print("is a VIDEO file : " + ext)
            file = os.path.basename(str(p))
            newpath = output_dir + os.sep + "videos" + os.sep + prefix + "_" + file
            i=0
            while os.path.exists(newpath):
                i = i + 1
                newpath = output_dir + os.sep + "videos" + os.sep + prefix + "_" + str(i) + "_" + file 
            print(newpath)
            if not os.path.exists(output_dir + os.sep + "videos" + os.sep):
                os.makedirs(output_dir + os.sep + "videos" + os.sep)
            #os.rename(p, newpath)
            copyfile(str(p), newpath)
        else:
            #print("is another file : " + ext)
            print("do nothing")
# break

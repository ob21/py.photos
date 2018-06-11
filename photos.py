from __future__ import unicode_literals
import os
from shutil import copyfile
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
parser.add_option("-p", "--prefix", dest="file_prefix",
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
file_prefix = ""
if options.input_dir is not None:
    input_dir = str(options.input_dir)
if options.output_dir is not None:
    output_dir = str(options.output_dir)
if options.file_prefix is not None:
    prefix = str(options.prefix)

print("input dir is " + input_dir)
logging.info("input dir is " + input_dir)
print("output dir is " + output_dir)
logging.info("output dir is " + output_dir)
print("prefix is " + file_prefix)
logging.info("prefix is " + prefix)

for p in Path(input_dir).glob('./**/*'):
    #print()
    #print(p)
    if p.is_file():
        ext = os.path.splitext(p)[1]
        img_types = [".JPG", ".JPEG", ".PNG", ".GIF"]
        vid_types = [".MOV", ".MP4", ".MPG", ".MPEG", ".AVI"]
        if ext in img_types:
            #print("is an IMAGE file : " + str(p))
            with open('.\\' + str(p), 'rb') as my_picture:
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
            file = os.path.basename(p)
            #print(file)
            newfile = prefix + "_" + file
            print("newfile = " + newfile)
            newpath = output_dir + "\\" + str(year) + "\\" + str(month) + "\\" + newfile
            i=0
            while os.path.exists(newpath):
                i = i + 1
                newpath = output_dir + "\\" + str(year) + "\\" + str(month) + "\\" + str(i) + "_" + newfile
            print(newpath)
            if not os.path.exists(output_dir + "\\" + str(year) + "\\" + str(month) + "\\"):
                os.makedirs(output_dir + "\\" + str(year) + "\\" + str(month) + "\\")
            #os.rename(p, newpath)
            copyfile(p, newpath)
        elif ext in vid_types:
            #print("is a VIDEO file : " + ext)
            file = os.path.basename(p)
            newpath = output_dir + "\\videos\\" + file_prefix + "_" + file
            i=0
            while os.path.exists(newpath):
                i = i + 1
                newpath = output_dir + "\\videos\\" + file_prefix + "_" + str(i) + "_" + file 
            print(newpath)
            if not os.path.exists(output_dir + "\\videos\\"):
                os.makedirs(output_dir + "\\videos\\")
            #os.rename(p, newpath)
            copyfile(p, newpath)
        else:
            #print("is another file : " + ext)
            print("do nothing")
# break

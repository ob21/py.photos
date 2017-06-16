from __future__ import unicode_literals
import os
import logging
from pathlib import Path
import exifread
from datetime import datetime
from datetime import date
from optparse import OptionParser
from pymediainfo import MediaInfo

# Needs Mediainfo dll win32 (.exe installer included in the project)

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
        img_types = [".JPG", ".JPEG", ".PNG", ".GIF"]
        vid_types = [".MOV", ".MP4", ".MPG", ".MPEG", ".AVI"]
        if ext in img_types:
            print("is an IMAGE file : " + str(p))
            with open('.\\' + str(p), 'rb') as my_picture:
                tags = exifread.process_file(my_picture)
                print('try to get exif data for ' + '.\\' + str(p))
                print("tags : "+str(tags))
                # print(str(tags.get('EXIF DateTimeOriginal')))
                try:
                    date = datetime.strptime(str(
                            tags.get('EXIF DateTimeOriginal')),
                            '%Y:%m:%d %H:%M:%S')
                except ValueError:
                    date = date.today()
                print("date = " + str(date))
                year = date.year
                print("year = " + str(year))
                month = date.month
                print("month = " + str(month))
            file = os.path.basename(p)
            print(file)
            # newfile = file.replace("593APPLE", "")
            # print("newfile = " + newfile)
            newpath = output_dir + "\\" + str(year) + "\\" + str(month) + "\\" + file
            print(newpath)
            if not os.path.exists(output_dir + "\\" + str(year) + "\\" + str(month) + "\\"):
                os.makedirs(output_dir + "\\" + str(year) + "\\" + str(month) + "\\")
            os.rename(p, newpath)
        elif ext in vid_types:
            print("is a VIDEO file : " + ext)
            year = None
            month = None
            if ext == ".MOV":
                media_info = MediaInfo.parse(str(p))
                found = 0
                for track in media_info.tracks:
                    # print(track)
                    if track.track_type == 'General':
                        print(track.encoded_date)
                        # print(track.tagged_date)
                        date = datetime.strptime(track.encoded_date, 'UTC %Y-%m-%d %H:%M:%S')
                        year = date.year
                        month = date.month
                        # print(year)
                        # print(month)
                        found = 1
                # print(found)
                if found == 1:
                    newpath = output_dir + "\\videos\\" + str(year) + "\\" + str(month) + "\\"
                    # print("year is not none")
                else:
                    newpath = output_dir + "\\videos\\"
            else:
                newpath = output_dir + "\\videos\\"
            print("newpath = " + newpath)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            try:
                os.rename(p, newpath + os.path.basename(p))
            except FileExistsError:
                print("Cannot override existing file : " + newpath + os.path.basename(p))
        else:
            print("is another file : " + ext)
            print("do nothing")
        # break

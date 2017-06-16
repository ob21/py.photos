from pymediainfo import MediaInfo
from datetime import datetime
from datetime import date

def print_frame(text):
    print("+-{}-+".format("-" * len(text)))
    print("| {} |".format(text))
    print("+-{}-+".format("-" * len(text)))

media_info = MediaInfo.parse("IMG_2623.MOV")
for track in media_info.tracks:
    print_frame(track.track_type)
    if track.track_type == 'General':
        print(track.encoded_date)
        print(track.tagged_date)
        print(track)
        date = datetime.strptime(track.encoded_date,
                            'UTC %Y-%m-%d %H:%M:%S')
        print(date.year)
        print(date.month)

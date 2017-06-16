from pymediainfo import MediaInfo

def print_frame(text):
    print("+-{}-+".format("-" * len(text)))
    print("| {} |".format(text))
    print("+-{}-+".format("-" * len(text)))

media_info = MediaInfo.parse("IMG_2206.MOV")
for track in media_info.tracks:
    print_frame(track.track_type)
    print(track.to_data())

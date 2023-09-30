import os
from shutil import rmtree
import ffmpeg
from pytube import YouTube
from pytube.cli import on_progress
from tabulate import tabulate

link = str(input("ENTER THE YOUTUBE URL :: "))

parent_dir = os.path.expanduser("~") + r"\Downloads"
file = YouTube(link, on_progress_callback=on_progress)
res_list = [['Index', 'Resolution', 'Identifier Code (itag)']]
abr_list = [['Index', 'Audio Bitrate', 'Identifier Code (itag)']]
title = file.title
special_characters = ('\\', ' / ', ':', '*', '?', '<', '>', '|', '\"', ' ')

for i in special_characters:
    title = title.replace(i, ".")

print(30 * '-')
print(f"Title: {file.title}\nChannel: {file.author}")
print(30 * '-')

download_dir = parent_dir + "\\" + title
temp_dir = download_dir + "\\" + "Temp"
if not os.path.exists(download_dir):
    os.mkdir(download_dir)
if not os.path.exists(temp_dir):
    os.mkdir(temp_dir)


def downloader(media, path, media_type):
    attribute = 'file property'
    att_list = []
    if media_type == 'video':
        attribute = 'RESOLUTION'
        att_list = [['Index', 'Resolution', 'Identifier Code (itag)']]
        for streams in media.streams.filter(only_video=True, mime_type="video/webm"):
            att_list.append([streams.resolution, streams.itag])
    elif media_type == "audio":
        attribute = 'AUDIO BITRATE'
        att_list = [['Index', 'Audio Bitrate', 'Identifier Code (itag)']]
        for streams in media.streams.filter(only_audio=True, mime_type="audio/webm"):
            att_list.append([streams.abr, streams.itag])

    print(f"\nAVAILABLE {attribute}\n")
    print(
        tabulate(att_list, headers='firstrow', showindex=True, tablefmt='fancy_grid', stralign='center',
                 numalign='center'))
    att_index = int(input("Please select an index :: "))
    att_itag = int(att_list[att_index + 1][1])
    print("Downloading...")
    media.streams.get_by_itag(att_itag).download(path, media_type + ".webm")

    print("\n", 30 * '-')


downloader(file, temp_dir, "video")
downloader(file, temp_dir, "audio")


(
    ffmpeg
    .input(temp_dir + r"\video.webm")
    .output(download_dir + "\\" + title + ".webm")
    .global_args('-i', temp_dir + r"\audio.webm")
    .global_args('-c', 'copy')
    .global_args('-map', '0:v:0')
    .global_args('-map', '1:a:0')
    .global_args('-hide_banner')
    .global_args('-v', 'warning')
    .global_args('-stats')
    .run()
)
rmtree(temp_dir)

# -*- coding: utf-8 -*-
# !/usr/bin/python3

# sudo apt install ffmpeg -y
# python3 -m pip install pytube --no-cache-dir
# python3 -m pip install --upgrade pytube

import os
import re
import shutil
import sys

from pytube import Playlist, YouTube


def main(playlistURL, folderPath):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Set Playlist
    p = Playlist(playlistURL)

    # Set number of total videos and numbering format
    numbTotal = len(p.video_urls)
    formatIdx = "{:0" + str(len(str(numbTotal))) + "}"

    # Check if folder already exists
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
    os.mkdir(folderPath)

    # Start from oldest to newest
    video_urls = reversed(p.video_urls)

    # Iterate over every video URL
    for idx, vodURL in enumerate(video_urls):
        # Get video
        video = YouTube(vodURL)

        # Set index format (001, 002, 003, ..., 323)
        idx = formatIdx.format(idx + 1)

        # Set filename, fullPath and temporary video/audio files
        # Set titles, allow only Alphanumeric and " .,_-" -> Remove multi-spaces
        title = re.sub('\s+', ' ', re.sub(r'[^A-Za-z0-9 .,_-]+', '', video.title))
        filename = idx + " - " + title
        fullPath = folderPath + filename + ".mp4"
        tmpVideo = folderPath + "tmp_video"
        tmpAudio = folderPath + "tmp_audio"

        # Show progress
        print("(" + str(round(int(idx) / numbTotal * 100, 2)) + "% - " + idx + "/" + str(numbTotal) + ") - " + title)

        # Download the best video quality
        print("Downloading video")
        video_only = video.streams.filter(type='video').order_by('resolution').last()
        video_only.download(filename=tmpVideo)

        # Download the best audio quality
        print("Downloading audio")
        audio_only = video.streams.filter(type='audio').order_by('abr').last()
        audio_only.download(filename=tmpAudio)

        # Merge two files
        print("Merging vidio-audio")
        cmd = "ffmpeg -i '" + tmpVideo + "' -i '" + tmpAudio + "' -c:v copy -c:a aac '" + fullPath + "' -loglevel error"
        os.system(cmd)

        # Remove tmp video/audio files
        os.remove(tmpVideo)
        os.remove(tmpAudio)

        print("")
    return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("script.py playlist folder")
        exit()

    main(sys.argv[1], sys.argv[2])

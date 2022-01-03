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


def download(vodURL, folderPath, idx, numbTotal):
    # Get video
    try:
        video = YouTube(vodURL)
    except Exception:
        print("ERROR - Couldn't reach video - " + vodURL)
        return False

    # Set filename, fullPath and temporary video/audio files
    # Set titles, allow only Alphanumeric and " .,_-" -> Remove multi-spaces
    title = re.sub('\s+', ' ', re.sub(r'[^A-Za-z0-9 .,_-]+', '', video.title))
    filename = idx + " - " + title
    fullPath = folderPath + filename + ".mp4"
    tmpVideo = folderPath + "tmp_video"
    tmpAudio = folderPath + "tmp_audio"

    # Show progress
    print("(" + str(round(int(idx) / int(numbTotal) * 100, 2)) + "% - " + str(idx) + "/" + str(numbTotal) + ") - " + title)

    try:
        # Download the best video quality
        print("INFO - Downloading video")
        video_only = video.streams.filter(type='video').order_by('resolution').last()
        video_only.download(filename=tmpVideo)

        # Download the best audio quality
        print("INFO - Downloading audio")
        audio_only = video.streams.filter(type='audio').order_by('abr').last()
        audio_only.download(filename=tmpAudio)

        # Merge two files
        print("INFO - Merging video-audio")
        cmd = "ffmpeg -i '" + tmpVideo + "' -i '" + tmpAudio + "' -c:v copy -c:a aac '" + fullPath + "' -loglevel error"
        os.system(cmd)

        # Remove tmp video/audio files
        os.remove(tmpVideo)
        os.remove(tmpAudio)

        print("INFO - Download Successful")
    except Exception:
        print("ERROR - Couldn't download Video, check URL")
        return False

    return True


def main(playlistURL, folderPath):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Set Playlist
    try:
        p = Playlist(playlistURL)
    except Exception:
        print("ERROR - Couldn't reach Playlist - " + playlistURL)
        return

        # Set number of total videos and numbering format
    numbTotal = len(p.video_urls)
    formatIdx = "{:0" + str(len(str(numbTotal))) + "}"

    # Check if folder already exists
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
    os.mkdir(folderPath)

    # Start from oldest to newest
    video_urls = reversed(p.video_urls)

    # Set Failed Video
    failedVideos, failedVideosAgain = {}, {}

    # Iterate over every video URL
    for idx, vodURL in enumerate(video_urls):
        # Set index format (001, 002, 003, ..., 323)
        idx = formatIdx.format(idx + 1)

        # Download Video
        status = download(vodURL, folderPath, idx, numbTotal)

        # Check for failed status
        if status is False:
            failedVideos[idx] = vodURL

        print("")

    # Check for Failed Videos
    print("--------------------------------")
    if len(failedVideos) != 0:
        totalFailed = formatIdx.format(len(failedVideos))
        print("INFO - Failed videos: " + totalFailed)
        print("INFO - Retrying")
        print("--------------------------------\n")

        # Retry for failed Videos
        for idx, vodURL in failedVideos.items():
            status = download(vodURL, folderPath, idx, totalFailed)
            if status is False:
                failedVideosAgain[idx] = vodURL

            print("")

    # Create log file for unsuccessful videos
    if len(failedVideosAgain) != 0:
        with open(folderPath + "log.txt", "w") as logFile:
            for idx, vodURL in failedVideosAgain.items():
                logFile.write(idx + " - " + vodURL + "\n")
        logFile.close()

    print("--------------------------------")
    print("INFO - Finished Downloading")
    print("INFO - Failed Videos: " + formatIdx.format(len(failedVideosAgain)))
    print("INFO - Location:" + sys.argv[2])
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("script.py playlist folder")
        exit()

    main(sys.argv[1], sys.argv[2])
    exit()

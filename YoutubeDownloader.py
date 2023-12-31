# -*- coding: utf-8 -*-
# !/usr/bin/python3

# sudo apt install ffmpeg -y

import os
import re
import shutil
import sys
from pytube import YouTube, Channel, Playlist


def checkURL():
    # Set Channel/Playlist
    try:
        p = Channel(YoutubeURL)
        print("INFO: Youtube Channel - " + p.channel_name)
    except Exception:
        try:
            p = Playlist(YoutubeURL)
            print("INFO: Playlist: " + p.title)
        except Exception:
            print("ERROR - Couldn't reach Channel or Playlist - " + YoutubeURL)
            return None

    return p


def download(vodURL):
    # Get video
    video = YouTube(vodURL)
    print("INFO - Video: " + video.title)

    # Download the best video quality
    print("INFO - Downloading video")
    video_only = video.streams.filter(type='video').order_by('resolution').last()
    video_only.download(filename=tmpVideo)

    # Download the best audio quality
    print("INFO - Downloading audio")
    audio_only = video.streams.filter(type='audio').order_by('abr').last()
    audio_only.download(filename=tmpAudio)

    return video


def process(video, idx):
    print("INFO - Processing")

    # Set filename, fullPath and temporary video/audio files
    # Set titles, allow only Alphanumeric and " .,_-" -> Remove multi-spaces
    title = re.sub('\s+', ' ', re.sub(r'[^A-Za-z0-9 .,_-]+', '', video.title)).strip()
    filename = idx + " - " + title
    fullPath = os.path.join(folderPath, filename + ".mp4")

    # Merge two files
    cmd = "ffmpeg -i '" + tmpVideo + "' -i '" + tmpAudio + "' -c:v copy -c:a aac '" + fullPath + "' -loglevel error"
    os.system(cmd)

    # Set modified date of file with video publication date
    pubDate = video.publish_date.timestamp()
    os.utime(fullPath, (pubDate, pubDate))

    # Remove tmp video/audio files
    os.remove(tmpVideo)
    os.remove(tmpAudio)


def writeLog(failedVideos):
    # Create log file for unsuccessful videos
    with open(os.path.join(folderPath, "log.txt"), "w") as logFile:
        for idx, vodURL in failedVideos.items():
            logFile.write(idx + " - " + vodURL + "\n")
    logFile.close()


def main():
    print("--------------------------------\n")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Check if folder already exists ? Empty : Create
    if os.path.exists(folderPath):
        shutil.rmtree(folderPath)
    os.mkdir(folderPath)

    # Start from oldest to newest | Failed videos track | Number total videos
    # Set number of total videos and numbering format
    video_urls, failedVideos = list(reversed(yt.video_urls)), {}
    formatIdx = "{:0" + str(len(str(len(video_urls)))) + "}"

    # Iterate over every video URL
    for idx, vodURL in enumerate(video_urls):
        # Set index format (001, 002, 003, ..., 323)
        idx = formatIdx.format(idx + 1)

        # Show progress
        percentage = str(round(int(idx) / len(video_urls) * 100, 2)) + "%"
        print(percentage + " - " + idx + "/" + str(len(video_urls)) + "(" + str(len(failedVideos)) + ") - " + vodURL)

        try:
            # Download Video -> Process video
            video = download(vodURL)
            process(video, idx)

            # Success
            print("INFO - Download Successful")
        except Exception:
            print("ERROR: Failed - " + vodURL)
            failedVideos[idx] = vodURL

        print("\n--------------------------------\n")

    # Create log file for unsuccessful videos
    if len(failedVideos) != 0:
        writeLog(failedVideos)

    print("--------------------------------")
    print("INFO - Finished Downloading")
    print("INFO - Failed Videos: " + formatIdx.format(len(failedVideos)))
    print("INFO - Location:" + sys.argv[2])

    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("script.py playlist folder")
        exit()

    # Global Variables
    YoutubeURL = sys.argv[1]
    folderPath = sys.argv[2]
    tmpVideo, tmpAudio = os.path.join(folderPath, "tmp_video"), os.path.join(folderPath, "tmp_audio")

    # Check YoutubeURL ? Run main : exit
    yt = checkURL()
    if yt:
        main()

    exit()

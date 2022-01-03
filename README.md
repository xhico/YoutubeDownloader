# YoutubeDownloader
 Download any public Youtube Channel / Playlist from Youtube</br>
 
# Features
 * Bulk download Youtube Channel
 * Bulk download Playlist
 * Automatic Numbering by oldest-to-newest (001 - VideoTitle1.mp4, 002 - VideoTitle2.mp4, ..., 232 - VideoTitle232.mp4)
 * Automatic detection, channel or playlist
 
## Dependencies
  * Pytube (https://pytube.io/en/latest/)
  * FFmpeg (https://www.ffmpeg.org/)

## Instalation
```
sudo apt install ffmpeg -y
```
```
python3 -m pip install pytube --no-cache-dir
```
```
python3 -m pip install --upgrade pytube
```

## Usage
```
python3 YoutubeDownloader.py https://www.youtube.com/playlist?list=PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc /home/pi/RickRoll/
```
```
python3 YoutubeDownloader.py https://www.youtube.com/c/RickastleyCoUkOfficial/videos /home/pi/RickRoll/
```

# PlaylistDownloader
 Download any public Playlist from Youtube</br>
 Automatic numbering (001 - VideoTitle1.mp4)
 
## Dependencies
  * Pytube (https://pytube.io/en/latest/)
  * FFmpeg (https://www.ffmpeg.org/)

## Instalation
```
sudo apt install ffmpeg -y
python3 -m pip install pytube --no-cache-dir
python3 -m pip install --upgrade pytube
```

## Usage
```
python3 PlaylistDownloader.py https://www.youtube.com/playlist?list=PLlaN88a7y2_plecYoJxvRFTLHVbIVAOoc /home/pi/RickRoll
```

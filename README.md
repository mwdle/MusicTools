# MusicTools  

A small collection of basic tools and scripts for management of a local music library.  

## Table of Contents  

* [Description](#musictools)  
* [M3U Playlist Generator](#playlist-generator)  
* [Repair File/Folder Name Utility](#name-normalizer)  
* [License](#license)  
* [Disclaimer](#disclaimer)  

## Playlist Generator  

This script allows you to quickly generate a .m3u playlist containing all music in a given folder and subfolders. Has support for excluding files/folders using regex.  
To learn more, execute the following from a shell in the same folder as this README:  

  ```shell
  python3 generatePlaylist.py --help
  ```  

  or  

  ```shell
  python3 generatePlaylist.py -h
  ```  

## Name Normalizer  

Some song, album, and artist names have characters that don't play nicely with some systems, resulting in poor portability of your music library when syncing across devices.  
This script automates the process of removing and replacing such characters from your music library.  
To learn more, execute the following from a shell in the same folder as this README:  

  ```shell
  python3 normalizeNames.py --help
  ```  

  or  

  ```shell
  python3 normalizeNames.py -h
  ```  

## License  
  
This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See the [LICENSE](LICENSE.txt) file for details.  
  
## Disclaimer  

This repository is provided as-is and is intended for informational and reference purposes only. The author assumes no responsibility for any errors or omissions in the content or for any consequences that may arise from the use of the information provided. Always exercise caution and seek professional advice if necessary.  

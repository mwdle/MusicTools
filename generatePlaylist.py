import os
import argparse
import re
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis

def get_duration(file_path):
    if file_path.lower().endswith('.mp3'):
        audio = MP3(file_path)
    if file_path.lower().endswith('.ogg'):
        audio = OggVorbis(file_path)
    return audio.info.length

def generate_m3u_playlist(playlist_directory, music_directory, output_file, exclusions):
    with open(f"{music_directory}{os.path.sep}{output_file}", 'w', encoding='utf-8') as playlist:
        playlist.write("#EXTM3U\n")
        for root, _, files in os.walk(playlist_directory):
            for file in files:
                if file.lower().endswith('.ogg') or file.lower().endswith('.mp3'):
                    song_path = os.path.join(root, file)
                    if exclusions != "" and re.search(exclusions, song_path):
                        continue
                    song_length = int(get_duration(song_path))
                    relative_path = os.path.relpath(song_path, music_directory)
                    playlist.write(f"#EXTINF:{song_length}, {file[:-4]}\n{relative_path}\n");

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="This script allows you to generate an m3u playlist given a folder containing music and/or subfolders with music. The following example generates a playlist called Jazz.m3u in /home/user/Media/Music containing all songs in the Jazz folder/subfolders: python3 generatePlaylist.py '/home/user/Media/Music/Jazz' '/home/user/Media/Music' 'Jazz.m3u'")
    parser.add_argument('playlist_directory', type=str, help="Path to the folder containing music/subfolders with music to add to the playlist.")
    parser.add_argument('music_directory', type=str, help="Path to the folder where you want to create the playlist file - the 'root' folder of your music library.")
    parser.add_argument('output_file', type=str, help="Name of m3u file (including .m3u extension). Example: 'Jazz.m3u'")
    parser.add_argument('exclusions', type=str, nargs='?', default="", help="(Optional) A regular expression to exclude specific folders and filenames from being added to the playlist. Leaving this empty will not exclude anything. The following example generates a playlist called 'Everything Except Jazz.m3u' containing all songs in the music library folder except those matching 'Jazz': python3 generatePlaylist.py '/home/user/Media/Music' '/home/user/Media/Music' 'Everything Except Jazz.m3u' 'Jazz'")
    
    args = parser.parse_args()
    
    generate_m3u_playlist(args.playlist_directory, args.music_directory, args.output_file, args.exclusions)
    print(f"Playlist generated: {args.music_directory}{os.path.sep}{args.output_file}")
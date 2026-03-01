import os
import yt_dlp
from tqdm import tqdm


def read_songs_from_txt(filename="songs.txt"):
    songs = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                songs.append(line)
    return songs


def download_song(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])


def main():
    os.makedirs("downloads", exist_ok=True)

    songs = read_songs_from_txt()

    total_songs = len(songs)

    if total_songs == 0:
        print("No songs found in songs.txt")
        return

    print(f"\nTotal songs available: {total_songs}")

    while True:
        try:
            limit = int(input("How many songs do you want to download? "))
            if 1 <= limit <= total_songs:
                break
            else:
                print(f"Enter a number between 1 and {total_songs}")
        except ValueError:
            print("Please enter a valid number.")

    songs_to_download = songs[:limit]

    print(f"\nDownloading {limit} song(s)...\n")

    for song in tqdm(songs_to_download, desc="Downloading Songs", unit="song"):
        try:
            download_song(song)
        except Exception:
            tqdm.write(f"Failed: {song}")


if __name__ == "__main__":
    main()
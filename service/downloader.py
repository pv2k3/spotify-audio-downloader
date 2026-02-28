import os
import yt_dlp
from config import AUDIO_FORMAT, AUDIO_QUALITY, OUTPUT_FOLDER


def file_already_exists(video_id: str) -> bool:
    """
    Check if a file with the same YouTube video ID already exists.
    """
    if not os.path.exists(OUTPUT_FOLDER):
        return False

    for file in os.listdir(OUTPUT_FOLDER):
        if video_id in file:
            return True
    return False


def download_audio(video_url: str):
    """
    Download audio only if not already present.
    """

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Extract info first (no download)
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        info = ydl.extract_info(video_url, download=False)
        title = info.get("title", "audio")
        video_id = info.get("id")

    if file_already_exists(video_id):
        print(f"⚠️ Already present: {title}")
        return

    print(f"⬇️ Downloading: {title}")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{OUTPUT_FOLDER}/%(title)s [%(id)s].%(ext)s",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": AUDIO_FORMAT,
                "preferredquality": AUDIO_QUALITY,
            }
        ],
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print("✅ Download complete")
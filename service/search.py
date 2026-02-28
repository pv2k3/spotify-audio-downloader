import yt_dlp

def search_youtube(query: str) -> str:
    """
    Searches YouTube and returns the first video URL.
    """
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "default_search": "ytsearch1",  # get first result
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        if "entries" in info:
            video = info["entries"][0]
        else:
            video = info

        return video["webpage_url"]
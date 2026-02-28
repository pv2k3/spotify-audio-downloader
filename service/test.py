from search import search_youtube
from downloader import download_audio


def download_from_search(query: str):
    print(f"Searching for: {query}")
    video_url = search_youtube(query)
    print(f"Found: {video_url}")
    print("Downloading best quality audio...")
    download_audio(video_url)
    print("Done!")


if __name__ == "__main__":
    search_query = input("Enter song name: ")
    download_from_search(search_query)
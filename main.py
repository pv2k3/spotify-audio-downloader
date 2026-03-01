from extract_tokens import extract_from_curl
from spotify_fetcher import SpotifyFetcher


def main():

    print("Step 1: Extracting tokens from curl...")
    extract_from_curl("curl_input.txt")

    print("Step 2: Fetching playlist data...")
    fetcher = SpotifyFetcher()

    try:
        data = fetcher.fetch_playlist()
        fetcher.save_to_file(data)
        print("Success! Playlist data saved to playlist_response.json")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
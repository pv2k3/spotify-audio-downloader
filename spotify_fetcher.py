import requests
import json


class SpotifyFetcher:

    def __init__(self, config_file="extracted_data.json"):
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)

        self.bearer_token = config["bearer_token"]
        self.client_token = config["client_token"]
        self.playlist_uri = config["playlist_uri"]

        self.url = "https://api-partner.spotify.com/pathfinder/v2/query"

        self.headers = {
            "accept": "application/json",
            "accept-language": "en",
            "app-platform": "WebPlayer",
            "authorization": f"Bearer {self.bearer_token}",
            "client-token": self.client_token,
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://open.spotify.com",
            "referer": "https://open.spotify.com/",
            "spotify-app-version": "1.2.85.301.g1a6ed5dd",
            "user-agent": "Mozilla/5.0"
        }

    def fetch_playlist(self, offset=0, limit=200):

        payload = {
            "variables": {
                "uri": self.playlist_uri,
                "offset": offset,
                "limit": limit,
                "enableWatchFeedEntrypoint": True
            },
            "operationName": "fetchPlaylist",
            "extensions": {
                "persistedQuery": {
                    "version": 1,
                    "sha256Hash": "9c53fb83f35c6a177be88bf1b67cb080b853e86b576ed174216faa8f9164fc8f"
                }
            }
        }

        response = requests.post(self.url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed: {response.status_code} - {response.text}")

    def save_to_file(self, data, filename="playlist_response.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
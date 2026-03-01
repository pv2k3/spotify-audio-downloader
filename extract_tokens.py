import re
import json


def extract_from_curl(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    bearer_match = re.search(r'authorization:\s*Bearer\s+([^\s"\^]+)', content, re.IGNORECASE)
    client_token_match = re.search(r'client-token:\s*([^\s"\^]+)', content, re.IGNORECASE)
    playlist_match = re.search(r'spotify:playlist:[a-zA-Z0-9]+', content)

    data = {
        "bearer_token": bearer_match.group(1) if bearer_match else None,
        "client_token": client_token_match.group(1) if client_token_match else None,
        "playlist_uri": playlist_match.group(0) if playlist_match else None
    }

    with open("extracted_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return data


if __name__ == "__main__":
    extract_from_curl("curl_input.txt")
    print("Extraction complete. Data saved to extracted_data.json")
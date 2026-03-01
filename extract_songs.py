import json


def extract_songs(input_file="playlist_response.json"):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data["data"]["playlistV2"]["content"]["items"]

    songs_list = []

    for item in items:
        try:
            track_data = item["itemV2"]["data"]

            song_name = track_data["name"]

            artist_name = track_data["artists"]["items"][0]["profile"]["name"]

            songs_list.append({
                "singer": artist_name,
                "song": song_name
            })

        except (KeyError, IndexError, TypeError):
            continue

    return songs_list


def save_to_json(songs, filename="songs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)


def save_to_txt(songs, filename="songs.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for song in songs:
            f.write(f"{song['singer']} - {song['song']}\n")


if __name__ == "__main__":
    songs = extract_songs()
    save_to_json(songs)
    save_to_txt(songs)

    print("Extraction complete.")
    print("Created:")
    print(" - songs.json")
    print(" - songs.txt")
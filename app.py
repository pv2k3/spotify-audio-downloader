import os
import json
import subprocess
import threading
import requests
from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
import yt_dlp
from tqdm import tqdm
import re
from urllib.parse import quote

app = Flask(__name__)
app.config['SONGS_FILE'] = 'songs.json'
app.config['DOWNLOADS_DIR'] = 'downloads'

# Create downloads directory if it doesn't exist
os.makedirs(app.config['DOWNLOADS_DIR'], exist_ok=True)


def load_songs():
    """Load songs from JSON file"""
    if os.path.exists(app.config['SONGS_FILE']):
        with open(app.config['SONGS_FILE'], 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_songs(songs):
    """Save songs to JSON file"""
    with open(app.config['SONGS_FILE'], 'w', encoding='utf-8') as f:
        json.dump(songs, f, indent=4, ensure_ascii=False)


def extract_tokens_from_curl(curl_command):
    """Extract bearer_token, client_token, and playlist_uri from curl command"""
    try:
        # Clean up PowerShell escape sequences
        cleaned = curl_command.replace('^"', '"').replace('^ ', ' ')
        
        # Extract tokens using same patterns as extract_tokens.py
        bearer_match = re.search(r'authorization:\s*Bearer\s+([^\s"]+)', cleaned, re.IGNORECASE)
        client_token_match = re.search(r'client-token:\s*([^\s"]+)', cleaned, re.IGNORECASE)
        playlist_match = re.search(r'spotify:playlist:[a-zA-Z0-9]+', cleaned)
        
        return {
            "bearer_token": bearer_match.group(1) if bearer_match else None,
            "client_token": client_token_match.group(1) if client_token_match else None,
            "playlist_uri": playlist_match.group(0) if playlist_match else None
        }
    except Exception as e:
        print(f"Error extracting tokens: {str(e)}")
        return None


def fetch_songs_from_curl(curl_command):
    """Fetch songs using curl command - uses SpotifyFetcher pattern"""
    try:
        # Extract tokens from curl command
        tokens = extract_tokens_from_curl(curl_command)
        if not tokens or not all(tokens.values()):
            return {"success": False, "message": "Could not extract bearer_token, client_token, or playlist_uri from curl command"}
        
        # Set up headers like SpotifyFetcher does
        headers = {
            "accept": "application/json",
            "accept-language": "en",
            "app-platform": "WebPlayer",
            "authorization": f"Bearer {tokens['bearer_token']}",
            "client-token": tokens['client_token'],
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://open.spotify.com",
            "referer": "https://open.spotify.com/",
            "spotify-app-version": "1.2.85.301.g1a6ed5dd",
            "user-agent": "Mozilla/5.0"
        }
        
        url = "https://api-partner.spotify.com/pathfinder/v2/query"
        
        # Prepare payload like SpotifyFetcher does
        payload = {
            "variables": {
                "uri": tokens['playlist_uri'],
                "offset": 0,
                "limit": 200,
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
        
        # Make the request
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            # Parse response using same pattern as extract_songs.py
            songs = parse_spotify_response(data)
            return {"success": True, "songs": songs}
        else:
            return {"success": False, "message": f"API request failed: {response.status_code}"}
    except requests.Timeout:
        return {"success": False, "message": "Request timeout"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)[:150]}"}


def parse_spotify_response(data):
    """Parse Spotify API response to extract songs"""
    try:
        songs = []
        items = data.get("data", {}).get("playlistV2", {}).get("content", {}).get("items", [])
        
        for item in items:
            try:
                track_data = item["itemV2"]["data"]
                song_name = track_data["name"]
                artist_name = track_data["artists"]["items"][0]["profile"]["name"]
                
                songs.append({
                    "singer": artist_name,
                    "song": song_name,
                    "downloaded": False,
                    "file_path": None,
                    "youtube_url": None
                })
            except (KeyError, IndexError, TypeError):
                continue
        
        return songs
    except Exception as e:
        return []


def get_youtube_search_url(singer, song):
    """Generate YouTube search URL for a song"""
    query = f"{singer} {song}".strip()
    return f"https://www.youtube.com/results?search_query={quote(query)}"


def is_song_downloaded(song):
    """Check if song is already downloaded - uses stricter matching"""
    if not os.path.exists(app.config['DOWNLOADS_DIR']):
        return False
    
    song_name = song.get('song', '').lower().strip()
    singer_name = song.get('singer', '').lower().strip()
    
    if not song_name or not singer_name:
        return False
    
    for file in os.listdir(app.config['DOWNLOADS_DIR']):
        if file.endswith('.mp3'):
            file_lower = file.lower()
            
            # Check if BOTH singer AND song name appear in filename (stricter match)
            if singer_name in file_lower and song_name in file_lower:
                song['downloaded'] = True
                song['file_path'] = file
                return True
    
    return False


def update_download_status():
    """Update download status for all songs"""
    songs = load_songs()
    for song in songs:
        is_song_downloaded(song)
    save_songs(songs)
    return songs


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/songs', methods=['GET'])
def get_songs():
    """Get all songs with accurate download status"""
    songs = load_songs()
    
    # Sync download status with actual files
    for song in songs:
        is_song_downloaded(song)
    
    # Save updated status
    save_songs(songs)
    
    return jsonify(songs)


@app.route('/api/songs/fetch', methods=['POST'])
def fetch_songs():
    """Fetch songs from curl command"""
    data = request.json
    curl_command = data.get('curl_command', '').strip()
    
    if not curl_command:
        return jsonify({"success": False, "message": "No curl command provided"})
    
    result = fetch_songs_from_curl(curl_command)
    
    if result['success']:
        # Add download status to fetched songs
        songs = result['songs']
        for song in songs:
            is_song_downloaded(song)
        
        # Save or update songs
        existing_songs = load_songs()
        
        # Merge with existing, avoiding duplicates
        song_keys = set()
        for song in existing_songs:
            key = f"{song['singer'].lower()}-{song['song'].lower()}"
            song_keys.add(key)
        
        for song in songs:
            key = f"{song['singer'].lower()}-{song['song'].lower()}"
            if key not in song_keys:
                existing_songs.append(song)
        
        save_songs(existing_songs)
        return jsonify({"success": True, "songs": existing_songs, "message": f"Fetched {len(songs)} songs"})
    else:
        return jsonify(result)


@app.route('/api/songs/load', methods=['POST'])
def load_existing_songs():
    """Load existing songs from songs.json"""
    songs = load_songs()
    for song in songs:
        is_song_downloaded(song)
    return jsonify({"success": True, "songs": songs})


@app.route('/api/download', methods=['POST'])
def download_song():
    """Download a single song"""
    data = request.json
    singer = data.get('singer', '').strip()
    song = data.get('song', '').strip()
    
    if not singer or not song:
        return jsonify({"success": False, "message": "Invalid song data"})
    
    query = f"{singer} - {song}"
    
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"downloads/%(title)s.%(ext)s",
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
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        
        # Update song status
        songs = load_songs()
        for s in songs:
            if s['singer'].lower() == singer.lower() and s['song'].lower() == song.lower():
                s['downloaded'] = True
                # Find the actual file path
                for file in os.listdir(app.config['DOWNLOADS_DIR']):
                    if file.endswith('.mp3'):
                        s['file_path'] = file  # Store only filename
                        break
                break
        save_songs(songs)
        
        return jsonify({"success": True, "message": f"Downloaded: {query}"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Download failed: {str(e)}"})


@app.route('/api/download/batch', methods=['POST'])
def download_batch():
    """Download multiple songs"""
    data = request.json
    songs_to_download = data.get('songs', [])
    
    if not songs_to_download:
        return jsonify({"success": False, "message": "No songs selected"})
    
    def download_worker():
        for item in songs_to_download:
            try:
                query = f"{item['singer']} - {item['song']}"
                ydl_opts = {
                    "format": "bestaudio/best",
                    "outtmpl": f"downloads/%(title)s.%(ext)s",
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
                    ydl.extract_info(f"ytsearch1:{query}", download=True)
                
                # Update status
                songs = load_songs()
                for s in songs:
                    if s['singer'].lower() == item['singer'].lower() and s['song'].lower() == item['song'].lower():
                        s['downloaded'] = True
                        # Find the actual file
                        for file in os.listdir(app.config['DOWNLOADS_DIR']):
                            if file.endswith('.mp3'):
                                s['file_path'] = file  # Store only filename
                                break
                        break
                save_songs(songs)
            except Exception as e:
                print(f"Failed to download {item['singer']} - {item['song']}: {str(e)}")
    
    # Start download in background thread
    thread = threading.Thread(target=download_worker)
    thread.daemon = True
    thread.start()
    
    return jsonify({"success": True, "message": "Downloads started in background"})


@app.route('/api/play/<path:filename>')
def play_song(filename):
    """Play a downloaded song"""
    try:
        file_path = os.path.join(app.config['DOWNLOADS_DIR'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='audio/mpeg')
        else:
            return jsonify({"success": False, "message": "File not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400


@app.route('/api/songs/clear', methods=['POST'])
def clear_songs():
    """Clear all songs"""
    save_songs([])
    return jsonify({"success": True, "message": "Songs cleared"})


@app.route('/api/songs/export', methods=['GET'])
def export_songs():
    """Export songs to text file"""
    songs = load_songs()
    content = "\n".join([f"{song['singer']} - {song['song']}" for song in songs])
    
    with open('songs.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return send_file('songs.txt', as_attachment=True, mimetype='text/plain')


@app.route('/api/youtube/search', methods=['POST'])
def youtube_search():
    """Get YouTube search URL for a song"""
    data = request.json
    singer = data.get('singer', '').strip()
    song = data.get('song', '').strip()
    
    if not singer or not song:
        return jsonify({"success": False, "message": "Invalid song data"})
    
    youtube_url = get_youtube_search_url(singer, song)
    
    # Also save it to songs.json
    songs = load_songs()
    for s in songs:
        if s['singer'].lower() == singer.lower() and s['song'].lower() == song.lower():
            s['youtube_url'] = youtube_url
            break
    save_songs(songs)
    
    return jsonify({"success": True, "youtube_url": youtube_url})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

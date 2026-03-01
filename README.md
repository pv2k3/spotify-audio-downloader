# 🎵 Spotify Audio Downloader

A modern web-based application to download songs from Spotify playlists with a beautiful dark-themed interface, built with Flask and Bootstrap.

## ✨ Features

- 🎯 **Paste Spotify Curl Command** - Fetch songs directly by pasting a curl command from Spotify API
- 📥 **Batch Download** - Download multiple songs at once in the background
- 🎧 **Built-in Player** - Play downloaded songs directly in the browser
- 🔍 **Search & Filter** - Easily find songs by name or artist
- 📊 **Pagination** - Browse songs with intuitive pagination (15 songs per page)
- 🌙 **Dark Theme** - Eye-friendly dark interface with modern styling
- ✅ **Download Tracking** - Automatically tracks which songs are downloaded
- 🔗 **YouTube Links** - One-click search on YouTube for any song
- 💾 **Persistent Storage** - All song data saved in JSON format
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

## 📋 Prerequisites

### Required
- **Python 3.8+**
- **FFmpeg** - Required for audio conversion to MP3

### FFmpeg Installation

**Windows (using Chocolatey):**
```powershell
choco install ffmpeg
```

**Windows (Manual):**
1. Download from: https://ffmpeg.org/download.html
2. Extract and add to System PATH
3. Verify: `ffmpeg -version`

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

## 🚀 Installation & Setup

### Step 1: Clone or Download the Project
```bash
cd spotify-audio-downloader
```

### Step 2: Create Virtual Environment (Optional but Recommended)
```powershell
python -m venv venv

# Activate it:
venv\Scripts\Activate.ps1
```

### Step 3: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Start the Application
```powershell
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 5: Open in Browser
Navigate to: **http://localhost:5000**

## 📖 How to Get the Spotify Curl Command

This is the most important step! Follow these instructions carefully:

### Method 1: From Spotify Web Player (Recommended)

1. **Open Spotify in your browser**
   - Go to: https://open.spotify.com
   - Log in with your Spotify account

2. **Navigate to Your Playlist**
   - Find and click on the playlist you want to download songs from

3. **Open Developer Tools**
   - Press: `F12` or `Right-click → Inspect`
   - Go to: **Network** tab

4. **Trigger a Network Request**
   - In the browser, scroll down in the playlist
   - You'll see network requests appearing

5. **Find the Spotify API Request**
   - Look for a request to `api-partner.spotify.com` or `api.spotify.com`
   - Click on it to open details

6. **Copy as cURL**
   - Right-click on the request
   - Select: **Copy → Copy as cURL**
   - Or find the **cURL** tab and copy the entire command

7. **Paste into the App**
   - The curl command should look like:
   ```
   curl "https://api-partner.spotify.com/pathfinder/v2/query" \
     -H "accept: application/json" \
     -H "authorization: Bearer BQA..." \
     -H "client-token: AACg8M..." \
     ...
   ```

### What the Curl Command Contains

The curl command includes:
- **Bearer Token** - Your Spotify authentication token
- **Client Token** - Spotify's client identifier
- **Playlist URI** - The unique identifier for your playlist
- **Headers** - Required API headers

**Important:** Tokens are temporary and expire after a few hours. Generate a new curl command when tokens expire.

### Detailed Visual Guide for Getting Curl Command

```
1. Open Spotify Web Player
   ↓
2. Right-click → Inspect (or F12)
   ↓
3. Click "Network" tab
   ↓
4. Scroll playlist to trigger API calls
   ↓
5. Look for "api-partner.spotify.com" request
   ↓
6. Right-click → Copy as cURL
   ↓
7. Paste in the app's text area
   ↓
8. Click "Fetch from Curl"
   ↓
9. Songs load! ✓
```

## 📱 How to Use the Application

### 1. Fetch Songs from Spotify

1. **Get your curl command** (see section above)
2. **Paste** it in the text area labeled "Paste Curl Command"
3. **Click** "Fetch from Curl"
4. Wait for songs to load...
5. All songs from the playlist will appear in the table ✅

### 2. Browse Songs

- **View Songs**: Songs are displayed in a table with:
  - Song name
  - Artist name
  - Download status (Downloaded/Pending)
  - Action buttons

- **Search**: Use the search box to find songs by:
  - Song name
  - Artist name
  - Any keyword

- **Pagination**: 
  - Shows 15 songs per page
  - Use page navigation buttons to browse
  - See page number and total songs

### 3. Select and Download

**Single Song:**
- Click the **Download** button (yellow) next to any pending song
- Wait for download to complete

**Multiple Songs:**
1. Check the boxes next to songs you want
2. Click **"Select All"** button (optional)
3. Click **"Download Selected"** button
4. Downloads happen in the background
5. Status updates automatically

**Keyboard Shortcut:**
- `Ctrl + Enter` - Download selected songs
- `Ctrl + A` - Select all songs

### 4. Play Downloaded Songs

- Click the **Play** button (blue) next to any downloaded song
- Audio player opens in a modal
- Use standard player controls (play, pause, volume, seek)

### 5. Search on YouTube

- Click the **YouTube** button (red) next to any song
- New tab opens with YouTube search results
- Find the official music video or audio version

### 6. Export Songs

- Click the **Export** button (top right)
- Downloads a `songs.txt` file with all song names and artists

## 🎨 UI Overview

```
┌─────────────────────────────────────────────────────────┐
│  🎵 Spotify Audio Downloader          [↺] [⬇️] [...]    │
├──────────────────┬──────────────────────────────────────┤
│  SIDEBAR         │  MAIN CONTENT                        │
├──────────────────┼──────────────────────────────────────┤
│ • Curl Input     │  Songs Table (Paginated)             │
│ • Buttons        │  - Page 1 of X                       │
│ • Search Box     │  - 15 songs per page                 │
│ • Quick Actions  │  - Pagination controls               │
│ • Song Counter   │                                      │
│                  │  Downloaded Songs Player             │
│                  │  - List of playable songs            │
└──────────────────┴──────────────────────────────────────┘
```

## 📁 Project Structure

```
spotify-audio-downloader/
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── songs.json                  # Songs database (auto-created)
├── songs.txt                   # Text export (auto-created)
├── templates/
│   └── index.html             # Main HTML interface
├── static/
│   ├── style.css              # Dark theme styling
│   └── script.js              # Frontend logic
├── downloads/                 # Downloaded MP3 files
│   └── (song files...)
└── .gitignore                 # Git configuration
```

## 🔧 API Endpoints

### GET /
Returns the main HTML interface

### GET /api/songs
Returns all songs with download status and file paths

### POST /api/songs/fetch
**Input:**
```json
{
  "curl_command": "curl \"https://...\" -H ..."
}
```
**Returns:** Fetched songs and existing songs merged

### POST /api/songs/load
Loads existing songs from songs.json

### POST /api/download
**Input:**
```json
{
  "singer": "Artist Name",
  "song": "Song Title"
}
```
Downloads a single song from YouTube

### POST /api/download/batch
**Input:**
```json
{
  "songs": [
    {"singer": "...", "song": "..."},
    {"singer": "...", "song": "..."}
  ]
}
```
Downloads multiple songs in background thread

### POST /api/youtube/search
**Input:**
```json
{
  "singer": "Artist Name",
  "song": "Song Title"
}
```
**Returns:** YouTube search URL

### GET /api/play/<filename>
Streams audio file for playing in browser

### GET /api/songs/export
Downloads songs.txt file

## ⚙️ Configuration

### Change Songs per Page

Edit `static/script.js`:
```javascript
let songsPerPage = 15; // Change to 10, 20, 25, etc.
```

### Change Port

Edit `app.py` at the bottom:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Change port here
```

### Audio Quality

Edit `app.py` in the download functions:
```python
"preferredquality": "192",  # Change to 128, 256, 320, etc.
```

## 🐛 Troubleshooting

### Issue: Port 5000 is Already in Use
**Solution:** Change the port in app.py:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: FFmpeg Not Found
**Solution:** 
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Linux: `sudo apt-get install ffmpeg`
- Verify: `ffmpeg -version`

### Issue: Download Fails
**Possible causes:**
- Song doesn't exist on YouTube
- No internet connection
- FFmpeg not installed
- Low disk space
- YouTube blocked in your region

### Issue: Can't Find Developer Tools
- Chrome/Edge: Press `F12`
- Firefox: Press `F12`
- Safari: CMD + Option + I

### Issue: Can't Get Curl Command
**Solution:** 
- Make sure you're on Spotify Web Player (https://open.spotify.com)
- Desktop Spotify app doesn't support this
- Check Network tab is selected
- Look for requests to `api-partner.spotify.com`

### Issue: Curl Command Works but No Songs Appear
**Possible causes:**
- Playlist is empty
- Tokens expired (try getting fresh curl command)
- Permission denied for playlist
- Network error - check browser console (F12)

## 📊 Songs Database (songs.json)

Each song entry contains:
```json
{
  "singer": "Artist Name",
  "song": "Song Title",
  "downloaded": false,
  "file_path": null,
  "youtube_url": null
}
```

- `downloaded` - Boolean flag for download status
- `file_path` - Filename of downloaded MP3 (null if not downloaded)
- `youtube_url` - YouTube search URL (generated when needed)

## 🔒 Security Notes

- Spotify tokens are extracted from curl command and used server-side only
- No tokens are stored permanently
- Downloaded files stored locally on your machine
- No data sent to external services except YouTube
- All API requests stay between your app and Spotify/YouTube

## 💾 File Sizes & Performance

- **Typical MP3** (3-4 min song @ 192kbps): **5-8 MB**
- **Entire playlist** (100 songs): **500 MB - 1 GB**
- **Keep at least 2-3 GB** free disk space

### Download Speed
- Single song: **2-5 seconds**
- 10 songs: **30-60 seconds**
- 50 songs: **4-8 minutes**
- Depends on internet speed and audio quality

## 🎯 Tips & Best Practices

1. **Always get fresh curl command** - Tokens expire after ~1 hour
2. **Download in batches** - Download 20-30 songs at a time, not all at once
3. **Check disk space** - Ensure you have enough space before downloading large playlists
4. **Use search** - Find specific songs quickly without scrolling
5. **Backup songs.json** - Keep a copy of your songs database
6. **Keep browser open** - App runs in browser, don't close the tab during downloads

## 📞 Support & Common Issues

### Curl Copy Methods for Different Browsers

**Google Chrome/Edge:**
1. Right-click request → Copy → Copy as cURL

**Firefox:**
1. Right-click request → Copy as cURL

**Safari:**
1. Click request → Response tab
2. Right-click → Copy as cURL

### Getting Fresh Tokens

Tokens expire after ~1 hour. If downloads fail:
1. Go back to Spotify Web Player
2. Refresh the page (F5)
3. Scroll the playlist to trigger new API requests
4. Get fresh curl command
5. Paste into app and try again

### Checking FFmpeg Installation

Open terminal/PowerShell and type:
```bash
ffmpeg -version
```

If you get "ffmpeg not found", FFmpeg is not properly installed.

## 📝 License

This project is for personal use and learning purposes only.

## 🙏 Credits

- Built with **Flask** (Python web framework)
- **Bootstrap 5** (UI framework)
- **yt-dlp** (YouTube downloader)
- **FFmpeg** (Audio conversion)
- Dark theme inspired by GitHub's dark mode

---

**Enjoy downloading and managing your Spotify music! 🎵**

**Last Updated:** March 1, 2026  
**Version:** 1.0 - Complete Feature Release

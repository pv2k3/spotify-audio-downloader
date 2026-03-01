# 🎵 Spotify Audio Downloader - Web Interface

A modern web-based frontend for downloading songs from Spotify playlists with a sleek dark theme interface built with Bootstrap.

## 🌟 Features

- ✅ **Paste Curl Command**: Paste a Spotify API curl command to fetch songs directly
- ✅ **Load Existing Songs**: Load songs from `songs.json` 
- ✅ **Download Tracking**: Track which songs have been downloaded
- ✅ **Built-in Player**: Play downloaded songs directly in the browser
- ✅ **Batch Downloading**: Select multiple songs and download them at once
- ✅ **Dark Theme**: Modern, eye-friendly dark interface with Bootstrap styling
- ✅ **Search/Filter**: Search songs by name or artist
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile devices
- ✅ **Export to TXT**: Export songs list to text file
- ✅ **Real-time Updates**: Status updates with loading indicators

## 📋 Prerequisites

- **Python 3.8+**
- **FFmpeg** (required for audio conversion)
- **pip** (Python package manager)

### Installing FFmpeg

**Windows (with Chocolatey):**
```powershell
choco install ffmpeg
```

**Windows (Manual):**
1. Download from https://ffmpeg.org/download.html
2. Extract and add to System PATH

**macOS (with Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

## 🚀 Installation & Setup

1. **Navigate to project directory:**
   ```bash
   cd spotify-audio-downloader
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   
   # Activate it:
   # Windows:
   venv\Scripts\activate
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **The web interface should load with the dark theme!**

## 📖 Usage Guide

### Getting Songs

There are two ways to populate the songs list:

#### Method 1: Load Existing Songs
- Click the **"Load Existing Songs"** button to load songs from `songs.json`
- This loads all previously saved songs

#### Method 2: Fetch from Spotify API (Curl)
1. Go to Spotify's playlist page
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh the page and look for a request to `api.spotify.com` or `api-partner.spotify.com`
5. Copy the curl command
6. Paste it in the **"Paste Curl Command"** textarea
7. Click **"Fetch from Curl"** button
8. Songs will be extracted and displayed

### Managing Songs

- **View Songs**: All songs display in the table with artist and title
- **Search**: Use the search box to filter songs by name or artist
- **Select Songs**: Check the boxes next to songs you want
- **Select All**: Click "Select All" button to select all displayed songs
- **Deselect All**: Click "Deselect All" to clear all selections

### Downloading

#### Download Single Song
- Click the **Download** button (⬇️) next to a pending song
- A status badge will show when complete

#### Download Multiple Songs
1. Select the songs you want to download (using checkboxes)
2. Click **"Download Selected"** button
3. Downloads will proceed in the background
4. Status will update automatically

### Playing Songs

1. Locate a song in the table with a **"Downloaded"** badge
2. Click the **Play** button (▶️) next to it
3. The player modal will open with the audio player
4. Or click any song in the **"Downloaded Songs Player"** section at the bottom

### Export

- Click the **Export** button (⬇️) in the top right to download `songs.json` as `songs.txt`

## 📁 Project Structure

```
spotify-audio-downloader/
├── app.py                      # Flask backend server
├── requirements.txt            # Python dependencies
├── songs.json                  # All songs database
├── songs.txt                   # Text version of songs
├── downloaded_tracks.txt       # Track of recent downloads
├── templates/
│   └── index.html             # Main HTML template
├── static/
│   ├── style.css              # Dark theme stylesheet
│   └── script.js              # Frontend logic
└── downloads/                 # Downloaded MP3 files
    └── (song files...)
```

## 🎨 Features Explained

### Dark Theme
The interface uses a carefully designed dark color scheme:
- Primary background: GitHub dark (#0d1117)
- Secondary background: Deep gray (#161b22)
- Accent colors: Green (success), Blue (info), Orange (warning)
- All optimized for eye comfort

### Bootstrap Integration
- Responsive grid layout that adapts to screen size
- Pre-built components: cards, tables, alerts, modals
- Smooth animations and transitions
- Accessibility-friendly

### Real-time Status Updates
- Download status tracked in `songs.json`
- Format:
  ```json
  {
    "singer": "Artist Name",
    "song": "Song Name",
    "downloaded": true,
    "file_path": "downloads/song_name.mp3"
  }
  ```

## 🔧 API Endpoints

### GET /
- Returns the main HTML interface

### GET /api/songs
- Returns all songs with download status

### POST /api/songs/fetch
- **Input**: `{ "curl_command": "curl ..." }`
- **Returns**: Fetched songs list

### POST /api/songs/load
- Loads existing songs from `songs.json`

### POST /api/download
- **Input**: `{ "singer": "...", "song": "..." }`
- Downloads a single song

### POST /api/download/batch
- **Input**: `{ "songs": [...] }`
- Downloads multiple songs in background

### GET /api/play/<filename>
- Streams song audio file

### GET /api/songs/export
- Exports songs to text file

## ⌨️ Keyboard Shortcuts

- **Ctrl/Cmd + Enter**: Download selected songs
- **Ctrl/Cmd + A**: Select all songs (in main page only)

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is occupied:
```python
# Edit app.py, change:
app.run(debug=True, host='0.0.0.0', port=5000)
# To:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### FFmpeg Not Found
Make sure FFmpeg is installed and added to PATH:
```bash
ffmpeg -version
```

### Download Fails
- Check internet connection
- Ensure song exists on YouTube (downloads use YouTube as source)
- Check FFmpeg installation
- Check available disk space

### Curl Request Fails
- Verify the curl command is correct
- Check if Spotify tokens are still valid
- Try refreshing the Spotify page to get a new curl

## 📝 Notes

- Songs are downloaded as MP3 files at 192kbps (good quality vs file size balance)
- Application requires internet connection for downloads
- Downloaded files are stored in the `downloads/` folder
- All song metadata is stored in `songs.json`
- The interface is fully responsive and mobile-friendly

## 🔒 Security Notes

- Curl data is parsed server-side for safety
- Authentication tokens from Spotify API are handled via curl input
- No tokens are stored locally in the web application
- Downloaded files are stored locally on your machine

## 📞 Support

For issues or feature requests:
1. Check the troubleshooting section
2. Verify dependencies are installed
3. Check console for error messages (F12 Developer Tools)
4. Review application logs in terminal

## 📄 License

This project is for personal use and learning purposes.

---

**Enjoy downloading and managing your Spotify music! 🎶**

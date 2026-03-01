# 🚀 Quick Start Guide

## ⚡ 60-Second Setup

### Windows
1. Make sure **FFmpeg** is installed: `ffmpeg -version`
2. Double-click `run.bat` file
3. Wait for browser to open at `http://localhost:5000`
4. Done! 🎉

### macOS / Linux
1. Make sure **FFmpeg** is installed: `ffmpeg -version`
2. Run: `chmod +x run.sh && ./run.sh`
3. Wait for browser to open
4. Done! 🎉

## 📝 How to Use

### Step 1: Get Your Curl Command
1. Go to https://open.spotify.com and log in
2. Open DevTools (F12 or Cmd+Option+I)
3. Go to **Network** tab
4. Click on your playlist
5. Look for a request to `api-partner.spotify.com`
6. Right-click → Copy as cURL

### Step 2: Fetch Songs
1. Paste the curl command in the **"Paste Curl Command"** box
2. Click **"Fetch from Curl"** button
3. Wait for songs to load

### Step 3: Download
- **Single song**: Click the **Download** button next to it
- **Multiple songs**: 
  - Check the boxes next to songs
  - Click **"Download Selected"**
  - Downloads start automatically

### Step 4: Play
- Click the **Play** button next to any downloaded song
- Audio player opens in a modal

## 🎵 Features at a Glance

| Feature | How to Use |
|---------|-----------|
| **Search** | Type in the search box to filter songs |
| **Select All** | Click "Select All" button |
| **Deselect All** | Click "Deselect All" button |
| **Download Multiple** | Select songs + click "Download Selected" |
| **Play Songs** | Click play button on downloaded songs |
| **Export** | Click Export button to download songs.txt |
| **Refresh** | Click Refresh button to reload songs |

## 🎨 Interface Overview

```
┌─────────────────────────────────────────────────────┐
│  🎵 Spotify Audio Downloader          [↺] [⬇️]      │  ← Navigation
├──────────────────┬──────────────────────────────────┤
│  SIDEBAR         │  MAIN CONTENT                    │
├──────────────────┼──────────────────────────────────┤
│ Fetch Settings   │  Songs Table                     │
├──────────────────┤  - Song Name                     │
│ Curl Input       │  - Artist                        │
│ Buttons          │  - Status (Downloaded/Pending)  │
│ Quick Actions    │  - Actions (Play/Download)      │
│ Search           │                                  │
│                  │  Downloaded Songs Player        │
└──────────────────┴──────────────────────────────────┘
```

## 🔑 Keyboard Shortcuts

- `Ctrl+Enter` (or `Cmd+Enter`): Download selected songs
- `Ctrl+A` (or `Cmd+A`): Select all songs

## ❌ Not Working?

**Port 5000 is busy?**
- Change port in `app.py` line 173 from `5000` to `5001`

**FFmpeg not found?**
- Windows: `choco install ffmpeg`
- macOS: `brew install ffmpeg`
- Ubuntu: `sudo apt install ffmpeg`

**Downloads fail?**
- Check internet connection
- Make sure FFmpeg is installed
- Check disk space

**Need help?**
- See the full README.md for detailed troubleshooting

## 📁 Where Are My Songs?

Downloaded MP3 files are saved in the `downloads/` folder.

Songs metadata is stored in `songs.json`.

## 🎯 Pro Tips

1. **Batch downloads**: Select 10+ songs at once and let it download in background
2. **Search while downloading**: You can search while downloads happen
3. **Export**: Use Export button to backup your songs list
4. **Refresh**: Always refresh after stopping the app to update statuses
5. **Dark mode**: Eyes friendly dark theme for late night downloads 🌙

## 🔒 Privacy Note

- Tokens from Spotify curl are parsed server-side only
- No data is sent to external servers
- Everything stays on your machine
- Songs.json contains only song names and artist info

---

**Ready to download? Start with your curl command!** 🎵
